from abc import ABC, abstractmethod
from IMagazzino import IMagazzino
import socket
import logging
from config import BUFFER_SIZE, BACKLOG
from SkeletonThread import SkeletonThread

class Skeleton(IMagazzino, ABC):
    def __init__(self, ip: str, port: int):
        self.ip = ip
        self.port = port
        self.bufsize = BUFFER_SIZE

    # Lascio l'implementazione al server effettivo
    ###################################################
    @abstractmethod
    def deposita(self, articolo: str, id: int) -> bool:
        pass

    @abstractmethod
    def preleva(self, articolo: str) -> int:
        pass
    ###################################################

    # Qui implemento la logica di comunicazione
    def runSkeleton(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

            s.bind((self.ip, self.port))
            s.listen(BACKLOG)

            logging.info(f"In ascolto su: {self.ip}/{s.getsockname()[1]}")

            while True:

                conn, addr = s.accept()
                logging.info(f"Accettata connessione da {addr}")

                # Qui devo passare `conn` a un Thread

                t = SkeletonThread(conn, self.bufsize, self)
                t.start()

