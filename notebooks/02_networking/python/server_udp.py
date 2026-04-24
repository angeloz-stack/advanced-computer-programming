from tkinter.filedialog import LoadFileDialog
import socket
import argparse
from loguru import logger
import sys
import time

logger.remove()
logger.add(sink=sys.stderr,format="{level} SERVER_UDP {message}")

IP = "0.0.0.0" # <-- In ascolto su tutte le interfacce
BUFFER_SIZE = 1024

def server(port: int, timeout: int):

    deadline = time.time() + timeout

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.bind((IP, port))
        logger.info(f"Server in ascolto su {IP}:{s.getsockname()[1]}")

        while True:

            time_left = deadline - time.time()
            if time_left <= 0:
                logger.info("Timeout")
                break

            s.settimeout(time_left)

            try:
                data, addr = s.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                logger.info("Timeout")
                break

            logger.info(f"Ricevuto messaggio: {data.decode('utf-8')} da {addr}")
            
            s.sendto(data, addr)
            logger.info(f"Inviato messaggio: {data.decode('utf-8')} a {addr}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=0, help="port")
    parser.add_argument("--timeout", type=int, default=20, help="timeout (secondi)")
    args = parser.parse_args()
    server(args.port, args.timeout)

if __name__ == "__main__":
    main()