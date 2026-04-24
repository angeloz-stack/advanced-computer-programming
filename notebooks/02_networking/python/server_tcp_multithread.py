from socket import socket
import socket
import argparse
from loguru import logger
import sys
import time
from threading import Thread

logger.remove()
logger.add(sink=sys.stderr,format="{level} SERVER_TCP {thread.name} {message}")

IP = "0.0.0.0" # <-- In ascolto su tutte le interfacce
BUFFER_SIZE = 1024


def worker(conn: socket.socket):

    with conn:
        data = conn.recv(BUFFER_SIZE)
        logger.info(f"Ricevuto messaggio: {data.decode("utf-8")}")

        to_client = data[::-1]
        conn.send(to_client)
        logger.info(f"Inviato messaggio: {to_client.decode("utf-8")}")


def server(port: int, backlog: int, timeout: int):

    deadline = time.time() + timeout

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        s.bind((IP, port))

        s.listen(backlog) # <-- Massimo backlog connessioni in attesa

        logger.info(f"In ascolto su {IP}:{s.getsockname()[1]}")

        while True:

            time_left = deadline - time.time()

            if time_left <= 0:
                logger.info("Timeout")
                break

            s.settimeout(time_left)

            try:
                conn, addr = s.accept()
            except socket.timeout:
                logger.info("Timeout")
                break

            logger.info(f"Connessione da {addr}")

            t = Thread(target=worker, args=(conn,))
            t.start()
    
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="port")
    parser.add_argument("--backlog", type=int, help="backlog")
    parser.add_argument("--timeout", type=int, help="timeout (secondi)")
    
    args = parser.parse_args()

    server(args.port, args.backlog, args.timeout)

if __name__ == "__main__":
    main()