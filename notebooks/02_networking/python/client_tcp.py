import socket
import argparse
from loguru import logger
import sys

logger.remove()
logger.add(sink=sys.stderr,format="{level} CLIENT_TCP {message}")

IP = "localhost" # <-- Server si trova sullo stesso computer
BUFFER_SIZE = 1024

def client(port: int, message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        s.connect((IP, port))
        logger.info(f"Connesso al server {IP}:{port}")

        s.send(message.encode("utf-8"))
        logger.info(f"Inviato messaggio: {message}")

        data = s.recv(BUFFER_SIZE)
        logger.info(f"Ricevuto messaggio: {data.decode('utf-8')}")

    return

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="port")
    parser.add_argument("--message", type=str, help="message")
    
    args = parser.parse_args()

    client(args.port, args.message)

if __name__ == "__main__":
    main()