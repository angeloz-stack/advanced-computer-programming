from threading import Thread
import socket
import json
import logging

class SkeletonThread(Thread):
    """
    Questo thread deve sostanzialmente:
    - ricevere il messaggio dalla connessione -> serve conn, recv -> serve bufsize
    - analizzare la richiesta
    - chiamare il metodo giusto per inoltrare la richiesta al server -> serve un riferimento al server
    """
    
    def __init__(self, sock: socket.socket, clientMsg: str, addr: tuple, bufsize: int, ref):
        super().__init__()
        self.sock = sock
        self.clientMsg = clientMsg
        self.addr = addr
        self.bufsize = bufsize
        self.ref = ref

    def run(self):

        request = json.loads(self.clientMsg.decode("utf-8"))

        metodo = request["metodo"]
        articolo = request["articolo"]

        
        if metodo == "deposita":
            id = request["id"]
            try:
                id = int(id)
                result = self.ref.deposita(articolo, id)
            except ValueError:
                logging.warning(f"Id {id} non valido")
                result = "ERROR"

        elif metodo == "preleva":
            result = self.ref.preleva(articolo)

        else:
            logging.warning(f"Metodo {metodo} non riconosciuto")
            result = "ERROR"

        self.sock.sendto(str(result).encode("utf-8"), self.addr)