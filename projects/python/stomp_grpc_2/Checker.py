from statistics import mean
import service_pb2_grpc
import service_pb2
import grpc
import stomp
import argparse
import logging
from multiprocessing import Queue
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

# da traccia "supera una determinata soglia"
# assumo che "supera" significhi strettamente maggiore

ALERT = "/topic/alert"

class MyServicer(service_pb2_grpc.TempertureAlertServiceServicer):
    def __init__(self, queue: Queue, lock: Lock, 
                 conn: stomp.Connection, temp_threshold: int):
        self.queue = queue
        self.lock = lock
        self.conn = conn
        self.temp_threshold = temp_threshold

    def stream_temp(self, request_iterator, context):
        
        i = 0
        RESPONSE = "NORMAL"
        for temp in request_iterator:
            logging.debug(f"{i}) Inserisco {temp.value}")
            self.queue.put(temp.value)

            # check valore
            if (temp.value > self.temp_threshold):
                logging.warning(f"Valore {temp.value} supera la soglia, invio ALERT")
                self.conn.send(ALERT, str(temp.value))
                RESPONSE = "ALERT"
            
            i+=1
        
        return service_pb2.StringMessage(value=RESPONSE)
    
    def get_average(self, request, context):
        temp_values = []
        logging.info("Svuoto la coda")
        with self.lock:
            while not self.queue.empty():
                temp_values.append(self.queue.get())

        average = mean(temp_values)

        return service_pb2.Average(value=average)
    

def main():
    logging.basicConfig(
        format="[CHECKER] - [%(threadName)s] - %(message)s",
        level=logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threshold", type=int, help="temperature threshold")
    parser.add_argument("-s", "--size", type=int, default=5, help="queue size")
    args = parser.parse_args() #args.threshold

    with stomp.Connection([("localhost", 61613)]) as conn:
        conn.connect(wait=True)
        queue = Queue(args.size)
        lock = Lock()

        server = grpc.server(ThreadPoolExecutor(max_workers=10))
        service_pb2_grpc.add_TempertureAlertServiceServicer_to_server(MyServicer(
            queue=queue, lock=lock, conn=conn, temp_threshold=args.threshold
        ), server)

        address = "localhost:0"

        port = server.add_insecure_port(address)
        logging.info(f"Server gRPC in ascolto sulla porta {port}")

        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    main()