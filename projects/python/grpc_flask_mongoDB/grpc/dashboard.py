import statistics_pb2
import statistics_pb2_grpc
import grpc
import argparse
import logging


def main():

    logging.basicConfig(format="[DASHBOARD] %(message)s",
                        level=logging.INFO)

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=str, help="porta")
    args = parser.parse_args()

    address = f"localhost:{args.port}"

    with grpc.insecure_channel(address) as channel:

        stub = statistics_pb2_grpc.StatisticsManagerStub(channel)

        logging.info("Richiedo informazioni dei sensori...")
        logging.info("Sensori ricevuti (e medie):")

        sensors = [sensor for sensor in stub.getSensors(statistics_pb2.Empty())]
        logging.info(sensors)

        for sensor in sensors:
            mean = stub.getMean(statistics_pb2.MeanRequest(
                sensor_id = sensor.sensor_id,
                data_type = sensor.data_type
            ))

            logging.info(f"ID sensore: {sensor.sensor_id} - Data type: {sensor.data_type} - Media: {mean.value}")
            sensors.append

if __name__ == "__main__":
    main()