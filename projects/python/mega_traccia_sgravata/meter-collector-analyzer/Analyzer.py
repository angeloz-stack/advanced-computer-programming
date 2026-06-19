import logging
import grpc
import stomp
import argparse
import service_pb2
import service_pb2_grpc
import multiprocessing as mp
from concurrent import futures as ft

MAX_QUEUE_SIZE = 5
DESTINATIONS = {
    "alert": "/topic/alert",
    "log": "/queue/log"
}

class ConsumerProcess(mp.Process):
    def __init__(self, threshold: int, queue: mp.Queue, n_total_readings, sum):
        super().__init__()
        self.threshold = threshold
        self.queue = queue
        self.n_total_readings = n_total_readings
        self.sum = sum

    def run(self):

        # aprire connessione stomp
        print("Processo consumatore running...")

        with stomp.Connection([("localhost", 61613)]) as conn:

            conn.connect(wait=True)

            while True:
                reading = self.queue.get()
                reading_value = reading.reading

                # stringa da mandare: zone-meterId-reading
                to_send = f"{reading.zone}-{reading.meterId}-{reading_value}"

                conn.send(DESTINATIONS["alert"] if reading_value >= self.threshold else DESTINATIONS["log"], to_send)

                with self.n_total_readings.get_lock():
                    self.n_total_readings.value += 1
                
                with self.sum.get_lock():
                    self.sum.value += reading_value

class MyServicer(service_pb2_grpc.AnalyzerServicer):

    def __init__(self, queue: mp.Queue, n_total_readings, sum):
        super().__init__()
        self.queue = queue
        self.n_total_readings = n_total_readings
        self.sum = sum

    def analyze(self, request_iterator, context):

        for reading in request_iterator:
            self.queue.put(reading)
  
        return service_pb2.StringMessage(value="OK")

    def get_stats(self, request, context):
        return service_pb2.Stats(
            n_total_readings = self.n_total_readings.value,
            avg = self.sum.value / self.n_total_readings.value
        )

def main():

    logging.basicConfig(
        format = "[ANALYZER] %(threadName)s - %(levelname)s - %(message)s",
        level = logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--threshold", type=int, help="threshold")
    args = parser.parse_args()

    # creiamo queue e values
    queue = mp.Queue(MAX_QUEUE_SIZE)
    n_total_readings = mp.Value("i", 0)
    sum = mp.Value("i", 0)

    # runniamo server grpc passandoglieli (costruttore servicer)

    address = "localhost:0"
    server = grpc.server(ft.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_AnalyzerServicer_to_server(
        MyServicer(queue, n_total_readings, sum),
        server
    )

    port = server.add_insecure_port(address)

    logging.info("Avvio processo consumatore...")
    consumer = ConsumerProcess(args.threshold, queue, n_total_readings, sum)
    consumer.start()
    
    
    logging.info(f"Server gRPC in ascolto sulla porta {port}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()