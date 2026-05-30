# Quando servono i lock attorno a una `mp.Queue`?

Confronto tra due server che usano entrambi `multiprocessing.Queue` come struttura dati condivisa, ma adottano **modelli di concorrenza diversi**. La domanda guida è: *servono lock espliciti o no?*

I due casi:

1. **`projects/stomp_grpc/server.py`** — server gRPC, gli handler girano in **thread** dello stesso processo (`ThreadPoolExecutor`). → **Servono i lock.**
2. **`projects/proxy_skeleton_stomp/serviceImpl.py`** + `serviceSkeleton.py` — per ogni connessione TCP viene fatto fork di un **processo** (`mp.Process`). → **Non servono i lock.**

---

## Premessa: cosa garantisce già `mp.Queue`

`multiprocessing.Queue` è progettato per essere condiviso tra processi (e tra thread) e offre **out of the box**:

- `put()` e `get()` **atomici** e *thread/process-safe*;
- comportamento **bloccante**: `put` su coda piena attende che ci sia spazio, `get` su coda vuota attende che arrivi un elemento — senza bisogno di condition variable scritte a mano;
- serializzazione tramite `pickle` per attraversare il confine dei processi.

Quindi sulla **struttura dati** in sé non c'è mai race condition, indipendentemente dal modello di concorrenza. Questo è il punto da cui partire: se decidiamo di mettere dei lock, **non è per proteggere la coda** — è per proteggere qualcos'altro.

---

## Caso 1 — gRPC + thread: i lock servono

```python
# projects/stomp_grpc/server.py
class Servicer(service_pb2_grpc.ServiceServicer):
    def __init__(self, queue, lock_prod, lock_cons):
        self.queue = queue
        self.lock_prod = lock_prod
        self.lock_cons = lock_cons

    def deposita(self, request, context):
        with self.lock_prod:
            self.queue.put({...})
            logging.info(f"Deposito di {request.id} ...")
        return service_pb2.StringMessage(value="deposited")

    def preleva(self, request, context):
        with self.lock_cons:
            item = self.queue.get()
            logging.info(f"Prelevato {item['id_articolo']} ...")
        return service_pb2.Item(...)

    def svuota(self, request, context):
        self.lock_prod.acquire()
        self.lock_cons.acquire()
        while not self.queue.empty():
            item = self.queue.get()
            logging.info(f"[SVUOTA] - Prelevato ...")
            yield service_pb2.Item(...)
        self.lock_cons.release()
        self.lock_prod.release()
```

### Perché servono

Il server gRPC esegue gli RPC handler in un **`ThreadPoolExecutor`**: più chiamate concorrenti girano come **thread** dentro lo **stesso processo**, condividendo la stessa istanza di `Servicer`, la stessa `self.queue` e — punto cruciale — lo **stesso `logging`** con i suoi handler/stream.

I lock qui servono a rendere **atomica la coppia** *(operazione sulla coda + log relativo)*. Senza i lock, due `deposita` concorrenti potrebbero produrre log con questo interleaving:

```
Deposito di 1 - Deposito di 2 - <prodotto1>!<prodotto2>!
```

ovvero righe mescolate, perché `logging.info` non è una singola scrittura atomica e tra il `put` e il log un altro thread può infilarsi. La coda resta consistente (la garantisce `mp.Queue`), ma **i log diventano inutilizzabili** per ricostruire l'ordine degli eventi. Il lock chiude questa finestra.

### Perché *due* lock e non uno solo

- Un solo lock condiviso serializzerebbe inutilmente produttori e consumatori, vanificando il parallelismo che `mp.Queue` già offre tra le due direzioni.
- Con un lock per i produttori e uno per i consumatori, un `deposita` e un `preleva` possono procedere **in parallelo**, mentre più `deposita` (o più `preleva`) tra loro sono serializzati — che è quello che vogliamo, e solo per il motivo "log coerente" descritto sopra.

### Perché *non* condition variable

Le condition variable servono quando devi implementare a mano "aspetta finché una certa condizione non è vera" (es. coda vuota / piena) su una struttura dati che da sola non sa farlo. Qui la `mp.Queue` **lo fa già**: `put` blocca su coda piena, `get` blocca su coda vuota. Riscrivere lo stesso meccanismo con `Condition` sarebbe duplicazione, oltre che fonte di bug.

### Il caso speciale di `svuota`

`svuota` drena tutti gli elementi e li streamma al client. È un'operazione che deve essere **isolata sia dai produttori sia dai consumatori** per la sua intera durata (altrimenti un `deposita` concorrente farebbe entrare nuovi elementi mentre stai svuotando, e un `preleva` ti ruberebbe elementi che stavi per emettere). Per questo prende **entrambi** i lock — ed è l'unico punto in cui la serializzazione totale è voluta.

---

## Caso 2 — Skeleton + processi: i lock NON servono

```python
# projects/proxy_skeleton_stomp/serviceImpl.py
class serviceImpl(serviceSkeleton):
    def __init__(self):
        self.queue = mp.Queue(QUEUE_SIZE)

    def preleva(self):
        id = self.queue.get()
        logging.info(f"Prelevato id: {id}")
        return id

    def deposita(self, id_articolo):
        self.queue.put(id_articolo)
        logging.info(f"Depositato id: {id_articolo}")
        return "deposited"
```

```python
# projects/proxy_skeleton_stomp/serviceSkeleton.py (estratto)
def skeleton_proc(conn, service_ref):
    data = conn.recv(1024).decode("utf-8")
    msg = json.loads(data)
    if msg["metodo"] == "deposita":
        response = service_ref.deposita(int(msg["id"]))
    else:
        response = str(service_ref.preleva())
    conn.send(response.encode("utf-8"))

class serviceSkeleton(Iservice, ABC):
    def runSkeleton(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            s.listen(5)
            while True:
                conn, addr = s.accept()
                p = mp.Process(target=skeleton_proc, args=(conn, self))
                p.start()
```

### Perché non servono

Per ogni connessione accettata viene spawnato un **`mp.Process`**, non un thread. Le conseguenze:

1. **La coda resta sicura per costruzione.** `mp.Queue` è proprio progettata per essere condivisa tra processi: `put`/`get` da processi diversi sono già atomici e serializzati internamente. Stesso identico fatto del Caso 1, ma qui è l'unica cosa di cui ci serve preoccuparci.
2. **Niente race sui log.** Ogni processo figlio ha il **proprio** sistema di logging, con i propri handler e il proprio file descriptor verso stdout. Non c'è una struttura `logging` *in-process* condivisa tra le richieste, quindi non esiste la finestra "due thread che scrivono sullo stesso handler" che giustificava i lock nel Caso 1. Le righe di processi diversi possono apparire in ordine inatteso sul terminale, ma non si **mescolano a metà riga** — è un effetto cosmetico di scheduling, non una corruzione di stato.
3. **Niente operazione "drena tutto".** Non c'è un equivalente di `svuota`. Ogni handler tocca **un solo elemento** della coda (un `put` o un `get`), che è già atomico.

In altre parole: il modello di concorrenza *process-per-request* sposta il problema della sincronizzazione **fuori dal codice applicativo**, dentro `mp.Queue`. Aggiungere lock qui sarebbe **rumore**: complicherebbe il codice senza prevenire alcun bug reale.

### Quando *avresti dovuto* aggiungerli anche qui

Se al posto di `mp.Process(target=skeleton_proc, ...)` avessi usato `threading.Thread(target=skeleton_proc, ...)`, ti saresti ritrovato nella stessa situazione del Caso 1 (thread che condividono il `logging` in-process) e i lock attorno alla coppia `put|get + logging.info` sarebbero serviti per gli stessi motivi.

---

## TL;DR

> I lock attorno a una `mp.Queue` servono **non** per proteggere la coda — che è già safe — ma per rendere **atomici insieme alla coda** gli effetti collaterali in-process condivisi tra gli esecutori concorrenti (tipicamente il logging). Se gli esecutori sono **processi separati**, quegli effetti collaterali non sono condivisi e i lock diventano inutili.

## Checklist pratica

Quando guardi del codice che usa `mp.Queue`, chiediti in ordine:

1. **Chi esegue gli handler?** Thread dello stesso processo, o processi separati?
2. **Ci sono effetti collaterali in-process** (logging, contatori, strutture in memoria) **eseguiti insieme al `put`/`get`** che vuoi vedere coerenti?
3. **Esiste un'operazione che tocca più elementi della coda** in una sequenza che deve essere isolata (drain, snapshot, swap)?

- Se (1) = thread **e** (2 oppure 3) sono presenti → servono lock, e probabilmente due (produttori/consumatori separati) per non perdere parallelismo.
- Se (1) = processi → quasi sempre **niente lock**: lascia fare a `mp.Queue`.
- Se nessuna delle precedenti → niente lock.
