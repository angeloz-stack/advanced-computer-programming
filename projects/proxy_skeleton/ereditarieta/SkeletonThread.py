from threading import Thread
import socket
import json
import logging

class SkeletonThread(Thread):
    """
    Questo thread deve sostanzialmente:
    - ricevere i messaggio dalla connessione -> serve conn, recv -> serve bufsize
    - analizzare la richiesta
    - chiamare il metodo giusto per inoltrare la richiesta al server -> serve un riferimento al server
    """
    
    def __init__(self, conn: socket.socket, bufsize: int, ref):
        super().__init__()
        self.conn = conn
        self.bufsize = bufsize
        self.ref = ref

    def run(self):

        with self.conn as c:
            data = c.recv(self.bufsize)

            request = json.loads(data.decode("utf-8"))

            metodo = request["metodo"]
            articolo = request["articolo"]

            
            if metodo == "deposita":
                id = request["id"]
                try:
                    id = int(id)
                    result = self.ref.deposita(articolo, id)
                except ValueError:
                    loggin.warning(f"Id {id} non valido")
                    result = "ERROR"

            elif metodo == "preleva":
                result = self.ref.preleva(articolo)

            else:
                logging.warning(f"Metodo {metodo} non riconosciuto")
                result = "ERROR"

        
            c.send(str(result).encode("utf-8"))