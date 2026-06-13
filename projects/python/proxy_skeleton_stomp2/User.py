from IPrinter import IPrinter
import socket
import json
import logging
import argparse
import random

PRINT_OPTIONS = ["bw", "gs", "color"]
NUM_REQS = 10
EXTS = ["txt", "doc"]
# /user/file_{NUM}.{estensione}

#helper func
def _generate_filename() -> str:
    return f"/user/file_{random.randint(0,100)}.{random.choice(EXTS)}"

class Proxy(IPrinter):
    def __init__(self, port):
        self.port = port

    def print(self, pathFile: str, tipo: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.port))
            
            request = json.dumps({"pathFile": pathFile, "tipo": tipo})
            logging.info(f"[PROXY] Invio: {request}")
            if s.send(request.encode("utf-8")):
                logging.debug("Sent ok")


def main():
    logging.basicConfig(
        format = "[USER] [%(threadName)s] - %(message)s",
        level=logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int)
    args = parser.parse_args()

    proxy = Proxy(args.port)

    for i in range(NUM_REQS):
        logging.debug(f"Richiesta: {i}")
        proxy.print(_generate_filename(), random.choice(PRINT_OPTIONS))

if __name__ == "__main__":
    main()  