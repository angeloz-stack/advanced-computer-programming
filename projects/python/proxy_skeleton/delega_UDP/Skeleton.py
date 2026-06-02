from abc import ABC, abstractmethod
from IMagazzino import IMagazzino
import socket
import logging
from config import BUFFER_SIZE
from SkeletonThread import SkeletonThread
from ServerImpl import ServerImpl

class Skeleton(IMagazzino):
    def __init__(self, ip: str, port: int, delegate: ServerImpl):
        self.ip = ip
        self.port = port
        self.bufsize = BUFFER_SIZE
        self.delegate = delegate

    # Chiamo il delegate
    ###################################################
    def deposita(self, articolo: str, id: int) -> bool:
        return self.delegate.deposita(articolo, id)

    
    def preleva(self, articolo: str) -> int:
        return self.delegate.preleva(articolo)
    ###################################################

    # Qui implemento la logica di comunicazione (UDP)
    def runSkeleton(self):
        
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            s.bind((self.ip, self.port))

            logging.info(f"In ascolto su: {self.ip}/{s.getsockname()[1]}")

            while True:

                msg, addr = s.recvfrom(self.bufsize)
                
                # Qui devo passare `conn` a un Thread

                t = SkeletonThread(s, msg, addr, self.bufsize, self)
                t.start()

