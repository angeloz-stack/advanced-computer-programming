from serviceProxy import serviceProxy
import stomp
import multiprocessing as mp
import logging
import json

# funzione target dei processi che il listener
# crea per ogni messaggi ricevuto
def proc_func(message, port):

    proxy = serviceProxy(port)

    conn = stomp.Connection([("localhost", 61613)])
    conn.connect()

    data = json.loads(message)

    metodo = data["metodo"]

    if metodo == "deposita":
        id = data["id"]

        # Qui deposito tramite proxy

        result = proxy.deposita(id)

    else:

        # Qui prelevo tramite proxy

        result = str(proxy.preleva())

    conn.send("/queue/risposta", result)

    conn.disconnect()


class dispatcherListener(stomp.ConnectionListener):
    """"
    Questo è il listener del dispatcher, che preleva dalla coda richieste e
    per ogni messaggio prelevato avvia un processo che inoltra la richiesta
    al server tramite proxy
    """
    
    def __init__(self, port):
        self.port = port
    
    def on_message(self, frame):

        logging.info(f"[LISTENER] Ricevuto {frame.body}")

        p = mp.Process(target=proc_func, args=(frame.body, self.port))

        p.start()