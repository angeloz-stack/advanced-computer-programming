import socket
import argparse
from loguru import logger
import sys

logger.remove()
logger.add(sink=sys.stderr,format="{level} CLIENT_UDP {message}")

IP = "localhost" # <-- Server si trova sullo stesso computer
BUFFER_SIZE = 1024

def client(port: int, message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        
        s.sendto(message.encode("utf-8"), (IP, port))
        logger.info(f"Inviato messaggio: {message}")
        
        data, addr = s.recvfrom(BUFFER_SIZE)
        logger.info(f"Ricevuto messaggio: {data.decode('utf-8')}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, help="port")
    parser.add_argument("--message", type=str, help="message")
    
    args = parser.parse_args()

    client(args.port, args.message)

if __name__ == "__main__":
    main()