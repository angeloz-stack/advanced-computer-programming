import service_pb2
import service_pb2_grpc
import logging
import random
import argparse
import grpc
import threading

NUM_THREADS = 10
METHODS = ["sell", "buy"]

def thd_func(stub):
    
    method = random.choice(METHODS)

    if method == "sell":
        product_id = random.randint(1,100)
        logging.info(f"Invio richiesta [sell id: {product_id}]")
        response = stub.sell(service_pb2.ProductId(id=product_id)) # response è StringMessage
        logging.info(f"Ricevuto {response.value}")
    elif method == "buy":
        logging.info(f"Invio richiesta [buy]")
        product = stub.buy(service_pb2.Empty())
        logging.info(f"Ricevuto prodotto con id: {product.id}")
    else:
        pass
    return

def main():

    logging.basicConfig(
        format="[CLIENT] - [%(threadName)s] - %(message)s",
        level=logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="grpc server port")

    args = parser.parse_args()

    address = f"localhost:{args.port}"
    with grpc.insecure_channel(address) as channel:
        stub = service_pb2_grpc.ProductManagerStub(channel)
        
        threads = []

        for i in range(NUM_THREADS):
            t = threading.Thread(target=thd_func, args=(stub,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    return


if __name__ == "__main__":
    main()