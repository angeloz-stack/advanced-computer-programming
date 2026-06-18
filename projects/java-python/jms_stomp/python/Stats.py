import stomp
from time import sleep
import logging
import multiprocessing as mp
from multiprocessing import Queue
from queue import Empty

STATS_FILENAME = "stats.txt"
TOPICS = {
    "tickets" : "/topic/tickets_topic",
    "stats" : "/topic/stats_topic"
}

class ProducerProcess(mp.Process):
    """Avviato a ogni messaggio sul topic tickets: inserisce
    il nome dell'artista nella coda condivisa (process-safe)."""

    def __init__(self, queue: Queue, artist: str):
        super().__init__()
        self.queue = queue
        self.artist = artist

    def run(self):
        print(f"[PRODUCER PROCESS] Inserisco in coda {self.artist}")
        self.queue.put(self.artist)

class ConsumerProcess(mp.Process):
    """Avviato a ogni messaggio Sold sul topic stats: svuota la coda,
    conta le occorrenze di ciascun artista e scrive il dizionario su file."""

    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue

    def run(self):
        print("[CONSUMER PROCESS] Svuoto la coda")

        stats = {}

        # Drena tutto cio' che e' presente nella coda in questo momento.
        # get_nowait() solleva Empty quando la coda e' vuota: cosi' il
        # processo termina invece di restare bloccato in attesa.
        while True:
            try:
                artist = self.queue.get_nowait()
            except Empty:
                break
            stats[artist] = stats.get(artist, 0) + 1

        with open(STATS_FILENAME, "a") as f:
            for artist, value in stats.items():
                f.write(f"{artist} {value}\n")

class StatsListener(stomp.ConnectionListener):

    def __init__(self, queue: Queue):
        super().__init__()
        self.queue = queue


    def on_message(self, frame):
        destination = frame.headers["destination"]
        msg = frame.body

        print(f"Destination: {destination}")

        if destination == TOPICS["tickets"]:
            # msg contiene il nome di un artista: avvio un processo
            # produttore che lo inserisce nella coda
            p = ProducerProcess(self.queue, msg)
            p.start()
        elif destination == TOPICS["stats"]:
            # solo se il valore e' "Sold" avvio un processo consumatore
            if msg == "Sold":
                p = ConsumerProcess(self.queue)
                p.start()
        else:
            logging.warning(f"Destination {destination} non valida!")

        return
    
    def on_connected(self, frame):
        print("Connesso!")

    def on_error(self, frame):
        print(f"Errore: {frame.body}")


def main():

    logging.basicConfig(
        format = "[STATS (LISTENER)] - %(levelname)s - %(message)s",
        level = logging.INFO
    )

    with stomp.Connection([("localhost", 61613)], auto_content_length=False) as conn:

        queue = Queue()

        conn.set_listener("", StatsListener(queue))
        conn.connect(wait=True)
        logging.info("Running")

        conn.subscribe(TOPICS["tickets"], id=1)
        conn.subscribe(TOPICS["stats"], id=2)

        while True:
            sleep(1)

    return

if __name__ == "__main__":
    main()