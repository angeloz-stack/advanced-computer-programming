from abc import ABC, abstractmethod
from IPrinter import IPrinter
import socket
import logging
from threading import Thread
import json

def thd_func(conn: socket.socket, ref):
    logging.debug("(Skeleton Thread) Running!")
    request = json.loads(conn.recv(1024).decode("utf-8"))
    pathFile = request["pathFile"]
    tipo =  request["tipo"]
    logging.debug(f"(Skeleton) Invoco print con {pathFile} - {tipo}")
    ref.print(pathFile, tipo)
    return


class Skeleton(IPrinter, ABC):
    @abstractmethod
    def print(self, pathFile: str, tipo: str) -> None:
        raise NotImplementedError
    
    def runSkeleton(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            s.listen(5)
            logging.info(f"In ascolto sulla porta: {s.getsockname()[1]}")
            
            while True:
                conn, address = s.accept()

                if conn:
                    logging.debug("Conn received")

                t = Thread(target=thd_func, args=(conn, self))
                t.start()