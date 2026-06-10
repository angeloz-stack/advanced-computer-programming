import service_pb2
import service_pb2_grpc
import logging
import grpc
import threading
import concurrent.futures as ft
import requests

ADDRESS = "http://127.0.0.1:5000/update_history" # server flask

class MyProductManagerServicer(service_pb2_grpc.ProductManagerServicer):
    def __init__(self):
        self.queue = []
        self.queue_size = 5
        self._lock = threading.Lock()
        self.prod_cond = threading.Condition(self._lock)
        self.cons_cond = threading.Condition(self._lock)

    def an_item_is_available(self):
        return not (len(self.queue) == 0)
    
    def a_space_is_available(self):
        return not (len(self.queue) == self.queue_size)
    
    def sell(self, request, context):
        id = request.id

        with self.prod_cond:
            self.prod_cond.wait_for(lambda: self.a_space_is_available())
            logging.debug(f"Coda pre deposito: {self.queue}")
            self.queue.append(id)
            logging.info(f"Depositato id: {id}")
            logging.debug(f"Coda post deposito: {self.queue}")
            
            self.cons_cond.notify()
        
        data = {"operation":"sell","serial_number":id}
        response = requests.post(ADDRESS, json=data)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.info(f"Errore nel salvataggio su HistoryManager - {response.status_code} - {response.text}")
        else:
            logging.info(f"Salvataggio di id: {id} su HistoryManager andato a buon fine - {response.status_code}")
        
        return service_pb2.StringMessage(value="OK")
    
    def buy(self, request, context):
        with self.cons_cond:
            self.cons_cond.wait_for(lambda: self.an_item_is_available())

            logging.debug(f"Coda pre prelievo: {self.queue}")
            id = self.queue.pop()
            logging.info(f"Prelevato id: {id}")
            logging.debug(f"Coda post prelievo: {self.queue}")
            
        data = {"operation":"buy","serial_number":id}
        response = requests.post(ADDRESS, json=data)    

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.info(f"Errore nel salvataggio su HistoryManager - {response.status_code} - {response.text}")
        else:
            logging.info(f"Salvataggio di id: {id} su HistoryManager andato a buon fine - {response.status_code}")   
        
        return service_pb2.ProductId(id=id)


def main():
    logging.basicConfig(
        format="[PRODUCT MANAGER] - [%(threadName)s] - %(message)s",
        level=logging.INFO
    )

    address = "localhost:0"
    server = grpc.server(ft.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_ProductManagerServicer_to_server(MyProductManagerServicer(), server)

    port = server.add_insecure_port(address)
    logging.info(f"In ascolto sulla porta: {port}")

    server.start()
    server.wait_for_termination(180.0)

if __name__ == "__main__":
    main()