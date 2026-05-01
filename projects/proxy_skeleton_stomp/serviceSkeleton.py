from abc import ABC, abstractmethod
from Iservice import Iservice
import socket
import logging
import multiprocessing as mp
import json

def skeleton_proc(conn: socket.socket, service_ref):

    # bufsize = 1024
    data = conn.recv(1024).decode("utf-8")
    msg = json.loads(data)

    logging.info(f"Ricevuto {msg}")
    
    metodo = msg["metodo"]

    if metodo == "deposita":
        id = int(msg["id"])
        response = service_ref.deposita(id)

    else:
        response = str(service_ref.preleva()) # preleva ritorna un int, faccio casting

    logging.info(f"Invio {response}")

    conn.send(response.encode("utf-8"))

# lo skeleton eredita dall'interfaccia
# ma non implementa i metodi, la cui
# implementazione è lasciata a ServerImpl
class serviceSkeleton(Iservice, ABC):

    # restano astratti
    ######################################
    @abstractmethod
    def preleva(self):
        raise NotImplementedError

    @abstractmethod
    def deposita(self, id_articolo: int):
        raise NotImplementedError
    ######################################
    
    # implemento la comunicazione. Questo skeleton si
    # interfaccia con il Proxy del dispatcher, senza
    # messaggi ma con connessione TCP

    def runSkeleton(self):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            
            logging.info(f"Running on port {s.getsockname()[1]}")

            s.listen(5) # backlog = 5

            while True:
                conn, addr = s.accept()

                p = mp.Process(target=skeleton_proc, args=(conn,self))
                p.start()  