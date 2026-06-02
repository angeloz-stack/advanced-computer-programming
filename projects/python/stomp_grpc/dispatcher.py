import stomp
import json
import multiprocessing
import config
import logging
import argparse
from time import sleep
import grpc
import service_pb2_grpc
import service_pb2


def proc_func(data, port):

    # il processo deve:
    # 1. creare la connessione per mandare risposte
    # 2. creare stub  +  conn per mandare rpc -> serve porta

    request  = json.loads(data)
    
    conn = stomp.Connection([("localhost", 61613)])
    conn.connect(wait=True)

    address = f"localhost:{port}"
    with grpc.insecure_channel(address) as channel:
        stub = service_pb2_grpc.ServiceStub(channel)

        if request["metodo"] == "deposita":
            id = request["id_articolo"]
            prodotto = request["prodotto"]
            
            esito = stub.deposita(service_pb2.Item(id=id, product=prodotto))
            logging.info(f"Deposito di {id} - {prodotto} avvenuto!")

            conn.send(config.QUEUE_RESPONSES, esito.value)
        
        elif request["metodo"] == "preleva":
            item = stub.preleva(service_pb2.Empty())
            id = item.id
            product = item.product
            data = {"id_articolo": id, "prodotto": product}
            logging.info(f"Prelevato {id} - {product} con successo!")
            conn.send(config.QUEUE_RESPONSES, json.dumps(data))

        elif request["metodo"] == "svuota":

            for item in stub.svuota(service_pb2.Empty()):
                id = item.id
                product = item.product
                data = {"id_articolo": id, "prodotto": product}
                logging.info(f"[SVUOTA] - Prelevato {id} - {product} con successo!")
                conn.send(config.QUEUE_RESPONSES, json.dumps(data))


class DispatcherListener(stomp.ConnectionListener):
    def __init__(self, port):
        self.port = port
    
    def on_message(self, frame):
        
        logging.info(f"Ricevuto : {frame.body}")

        p = multiprocessing.Process(target=proc_func, args=(frame.body, self.port,))
        p.start()

def main():
    logging.basicConfig(format="[DISPATCHER] - %(processName)s - %(message)s",
                        level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=str, help="Porta per server gRPC")
    args = parser.parse_args()

    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener("", DispatcherListener(port=args.port))

    conn.connect(wait=True)
    conn.subscribe(config.QUEUE_REQUESTS, id=1)

    while True:
        sleep(1)

if __name__ == "__main__":
    main()

    
        