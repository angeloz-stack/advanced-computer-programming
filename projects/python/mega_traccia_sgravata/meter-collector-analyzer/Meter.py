from ICollector import ICollector
import json
import socket
import logging
from time import sleep
import random
import argparse
import threading

N_REQS = 4
N_THREADS = 5
ZONES = ["north",  "south"]

class Proxy(ICollector):

    def __init__(self, port: int):
        self.port = port

    def submit(self, meterId: int, zone: str, reading: int) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.port))
            to_send = json.dumps({
                "meterId": meterId,
                "zone": zone,
                "reading": reading
                })
            
            logging.info(f"Invio: {to_send}")

            s.send(to_send.encode("utf-8"))


def thd_func(proxy: Proxy, id):
    for _ in range(N_REQS):
        sleep(1)
        params = {
            "meterId": id,
            "zone": random.choice(ZONES),
            "reading": random.randint(50, 100)
        }
        proxy.submit(params["meterId"], params["zone"], params["reading"])
    
    return


def main():

    logging.basicConfig(
        format = "[METER] %(threadName)s - %(levelname)s - %(message)s",
        level = logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="gRPC server port")
    args = parser.parse_args()

    threads = []

    proxy = Proxy(args.port)

    for i in range(N_THREADS):

        t = threading.Thread(target=thd_func, args=(proxy, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()