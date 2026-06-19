from ICollector import ICollector
import json
import socket
import logging
from threading import Lock, Condition, Thread
from abc import ABC, abstractmethod
import grpc
import argparse
import service_pb2
import service_pb2_grpc
from time import sleep

BUFFER_SIZE = 1024
MAX_QUEUE_SIZE = 5

# Funzione helper
def _generate_iterator(stream):
    for el in stream:
        yield el

# FUNZIONI THREAD
################################################################################
def skeleton_thd_func(conn: socket.socket, ref):
    request = json.loads(conn.recv(BUFFER_SIZE).decode("utf-8"))
    ref.submit(request["meterId"], request["zone"], request["reading"])

def consumer_thd_func(port: int, ref):
    address = f"localhost:{port}"

    with grpc.insecure_channel(address) as channel:
        stub = service_pb2_grpc.AnalyzerStub(channel)

        readings_stream = []

        while True:
            if len(readings_stream) == 5:
                logging.info("[CONSUMER] - Raggiunte 5 letture, invio...")
                response = stub.analyze(_generate_iterator(readings_stream))
                logging.info(f"Ricevuto dopo stream: {response.value}")
                readings_stream.clear()

                sleep(3)

                stats = stub.get_stats(service_pb2.Empty())
                logging.info(f"""Statistiche ottenute:
                            Numero di letture totale: {stats.n_total_readings}
                            Valore medio delle letture: {stats.avg}""")

            # dalla coda prelevo f"{zone}-{meterId}-{reading}"
            items = ref.preleva().split("-")
            logging.info(f"[CONSUMER] Prelevato dalla coda {items}")

            readings_stream.append(service_pb2.Reading(
                meterId = int(items[1]),
                zone = items[0],
                reading = int(items[2])
            ))

################################################################################

# SKELETON
################################################################################
class Skeleton(ICollector, ABC):
    @abstractmethod
    def submit(self, meterId: int, zone: str, reading: int) -> None:
        raise NotImplementedError
    
    def runSkeleton(self, port: int):
        logging.info("Avvio processo consumatore...")
        consumer = Thread(target=consumer_thd_func, args=(port,self))
        consumer.start()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            s.listen(10)
            
            logging.info(f"In ascolto sulla porta {s.getsockname()[1]}")

            while True:
                conn, address = s.accept()
                t = Thread(target=skeleton_thd_func, args=(conn, self))
                t.start()
################################################################################

# IMPLEMENTAZIONE DEL COLLECTOR
################################################################################
class Collector(Skeleton):
    def __init__(self, queue_size: int):
        _lock = Lock()
        self.prod_cond = Condition(_lock)
        self.cons_cond = Condition(_lock)
        self.max_queue_size = queue_size
        self.coda = []

    def an_item_is_available(self):
        return not len(self.coda) == 0

    def a_space_is_available(self):
        return not len(self.coda) == self.max_queue_size
    
    def preleva(self) -> str:
        with self.cons_cond:
            self.cons_cond.wait_for(lambda: self.an_item_is_available())
            item = self.coda.pop(0)
            self.prod_cond.notify()
        
        return item
    
    def inserisci(self, measure: str) -> None:
        with self.prod_cond:
            self.prod_cond.wait_for(lambda: self.a_space_is_available())
            self.coda.append(measure)
            self.cons_cond.notify()

    # domanda: posso passare al thread come target direttamente la funzione
    # inserisci? visto che producer_thd_func fa solo quello -> oneline

    def submit(self, meterId: str, zone: str, reading: int) -> None:
        measure_concat = f"{zone}-{meterId}-{reading}"
        t = Thread(target=self.inserisci, args=(measure_concat,))
        t.start()


def main():

    logging.basicConfig(
        format = "[COLLECTOR] %(threadName)s - %(levelname)s - %(message)s",
        level = logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="gRPC server port")
    args = parser.parse_args()

    collector = Collector(MAX_QUEUE_SIZE)
    collector.runSkeleton(args.port)

if __name__ == "__main__":
    main()

        



        

    

