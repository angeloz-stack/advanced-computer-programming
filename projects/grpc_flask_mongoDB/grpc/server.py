import statistics_pb2
import statistics_pb2_grpc
import grpc
import pymongo
import logging
import statistics
from concurrent import futures as ft

class MyServicer(statistics_pb2_grpc.StatisticsManagerServicer):
    def __init__(self, database: pymongo.database.Database):
        self.database = database
    
    def getSensors(self, request, context):
        
        collection = self.database["sensors"]
        sensors = collection.find()

        for sensor in sensors:
            yield statistics_pb2.Sensor(
                sensor_id = int(sensor["_id"]),
                data_type = sensor["data_type"]
            )

    def getMean(self, request, context):
        
        sensor_id = request.sensor_id
        data_type = request.data_type

        if data_type == "temp":
            collection_target = "temp_data"
        elif data_type == "press":
            collection_target = "press_data"

        collection = self.database[collection_target]

        data = collection.find({"sensor_id": sensor_id})
        mean = statistics.mean([d["data"] for d in data])

        return statistics_pb2.StringMessage(value=str(mean))
        

def main():

    logging.basicConfig(format="[SERVER RPC] %(message)s",
                        level=logging.INFO)
    
    with pymongo.MongoClient("localhost", 27017) as client:

        db = client["database"]

        server = grpc.server(ft.ThreadPoolExecutor(max_workers=10))
        statistics_pb2_grpc.add_StatisticsManagerServicer_to_server(MyServicer(db), server)

        address = f"localhost:0"
        port = server.add_insecure_port(address)
        logging.info(f"In ascolto sulla porta {port}")

        server.start()
        server.wait_for_termination()

if __name__ == "__main__":
    main()