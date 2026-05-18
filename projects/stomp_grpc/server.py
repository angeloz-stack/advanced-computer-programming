import multiprocessing as mp
from concurrent import futures as ft
import config
import grpc
import logging
import service_pb2
import service_pb2_grpc

class Servicer(service_pb2_grpc.ServiceServicer):
    def __init__(self, queue, lock_prod, lock_cons):
        self.queue = queue
        self.lock_prod = lock_prod
        self.lock_cons = lock_cons

    def deposita(self, request, context):

        with self.lock_prod:
            self.queue.put({
                "id_articolo": request.id,
                "prodotto": request.product
            })
            logging.info(f"Deposito di {request.id} - {request.product} avvenuto con successo!")
        
        return service_pb2.StringMessage(value="deposited")
    
    def preleva(self, request, context):
        
        with self.lock_cons:
            item = self.queue.get()
            logging.info(f"Prelevato {item["id_articolo"]} - {item["prodotto"]}!")
        
        
        return service_pb2.Item(id = item["id_articolo"], product=item["prodotto"])


    def svuota(self, request, context):

        self.lock_prod.acquire()
        self.lock_cons.acquire()

        while not self.queue.empty():
            item = self.queue.get()
            logging.info(f"[SVUOTA] - Prelevato {item["id_articolo"]} - {item["prodotto"]}!")
            yield service_pb2.Item(id = item["id_articolo"], product=item["prodotto"])

        self.lock_cons.release()
        self.lock_prod.release()


def main():
    logging.basicConfig(format="[SERVER] - %(message)s",
                        level=logging.INFO)

    queue = mp.Queue(config.QUEUE_SIZE)
    lock_prod = mp.Lock()
    lock_cons = mp.Lock()

    server = grpc.server(ft.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ServiceServicer_to_server(Servicer(queue, lock_prod, lock_cons), server)

    port = server.add_insecure_port("localhost:0")
    server.start()
    logging.info(f"In ascolto sulla porta {port}")
    server.wait_for_termination()

if __name__ == "__main__":
    main()
