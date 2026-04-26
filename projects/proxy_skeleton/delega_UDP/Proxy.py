import socket
import json
import logging
from IMagazzino import IMagazzino
from config import BUFFER_SIZE

class Proxy(IMagazzino):
    def __init__(self, ip: str, port: int):
        self.ip = ip # ip destinazione
        self.port = port # porta destinazione
        self.buf_size = BUFFER_SIZE

    def deposita(self, articolo: str, id: int) -> bool:

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            addr = (self.ip, self.port)
            
            toSend = {"metodo": "deposita", "articolo": articolo, "id": id}
            data = json.dumps(toSend)

            logging.info(f"Invio {data} a {addr}")

            s.sendto(data.encode("utf-8"), addr)

            response, _ = s.recvfrom(self.buf_size)

            return False if response == "ERROR" else True

    def preleva(self, articolo: str) -> int:

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:

            addr = (self.ip, self.port)

            toSend = {"metodo": "preleva", "articolo": articolo}
            data = json.dumps(toSend)

            logging.info(f"Invio {data} a {addr}")

            s.sendto(data.encode("utf-8"), addr)

            response, _ = s.recvfrom(self.buf_size)

            return int(response)