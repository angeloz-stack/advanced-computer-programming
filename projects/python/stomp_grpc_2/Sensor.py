import service_pb2_grpc
import service_pb2
import grpc
import argparse
import logging
import random

LEN_TEMPERATURE_STREAM = 5 # numero di valori temperatura da mandare **per ogni** richiesta

def generate_temperature_stream():
    temps = [service_pb2.Temperature(value = random.randint(50,100)) for i in range(LEN_TEMPERATURE_STREAM)]
    for temp in temps:
        yield temp

def main():
    logging.basicConfig(
        format="[SENSOR] - %(message)s",
        level=logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="gRPC server port")
    args = parser.parse_args() #args.port

    address = f"localhost:{args.port}"

    with grpc.insecure_channel(address) as channel:
        stub = service_pb2_grpc.TempertureAlertServiceStub(channel)

        for i in range(1, 11):
            if i%2 == 0: # numero pari
                average = stub.get_average(service_pb2.Empty()) # qui ricevo la media
                logging.info(f"[Chiamata get_average] Ricevuto {average.value:.2f}")
            else:
                esito = stub.stream_temp(generate_temperature_stream()) # qui ricevo NORMAL/ALERT
                logging.info(f"[Chiamata stream_temp] Ricevuto {esito.value}")
                

if __name__ == "__main__":
    main()