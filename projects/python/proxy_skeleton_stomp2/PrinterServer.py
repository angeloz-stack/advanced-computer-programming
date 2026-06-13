from Skeleton import Skeleton
import json
import logging
from multiprocessing import Process, Queue
import stomp
from time import sleep

# map tipo di stampa e """stampante"""
PRINTER_MAPPING = {
    "bw": "/queue/bw",
    "gs": "/queue/bw",
    "color": "color"
}

def prod_proc_func(pathFile: str, tipo: str, queue: Queue):
    print("here i am")
    logging.debug("Producer process running!")
    item = json.dumps({"pathFile": pathFile, "tipo": tipo})
    logging.info(f"Inserisco nella coda di stampa path: {pathFile} tipo: {tipo}")
    queue.put(item)
    print("done")

"""def cons_proc_func(queue: Queue, conn: stomp.Connection):
    logging.info("Running!")
    
    while True:
        msg_string = queue.get()
        msg_data = json.loads(msg_string)
        logging.info(f"Prelevato dalla coda di stampa path: {msg_data["pathFile"]} tipo: {msg_data["tipo"]}")

        conn.send(PRINTER_MAPPING[msg_data["tipo"]], msg_string)
        sleep(1)
"""

class ConsumerProcess(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue

    def run(self):
        logging.info("Consumer process Running!")

        with stomp.Connection([("localhost", 61613)]) as conn:
            conn.connect(wait=True)
        
            while True:
                msg_string = self.queue.get()
                msg_data = json.loads(msg_string)
                logging.info(f"Prelevato dalla coda di stampa path: {msg_data["pathFile"]} tipo: {msg_data["tipo"]}")
                print(f"Prelevato dalla coda di stampa path: {msg_data["pathFile"]} tipo: {msg_data["tipo"]}")

                conn.send(PRINTER_MAPPING[msg_data["tipo"]], msg_string)
                sleep(1)

class PrinterServer(Skeleton):
    def __init__(self, queue: Queue):
        self.queue = queue

    def print(self, pathFile: str, tipo: str):
        logging.debug("Print invoked")
        p = Process(target=prod_proc_func, args=(pathFile, tipo, self.queue))
        p.start()

def main():
    logging.basicConfig(
        format="[SERVER] - %(processName)s - %(message)s",
        level = logging.INFO
    )

    queue = Queue(maxsize=10)

    logging.info("Avvio il processo consumatore...")
    p = ConsumerProcess(queue=queue)
    p.start()

    printerServer = PrinterServer(queue)
    printerServer.runSkeleton()

if __name__ == "__main__":
    main()  