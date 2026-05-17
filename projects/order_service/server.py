import grpc
import logging
import random
from concurrent import futures
import order_management_pb2
import order_management_pb2_grpc

class OrderManagementServicer(order_management_pb2_grpc.OrderManagementServicer):
    def __init__(self):
        self.orders_dict = {}
        
    # unary RPC
    def addOrder(self, request, context):
        id = random.randint(1,600)
        request.id = str(id)
        self.orders_dict[request.id] = request
        logging.info(f"Aggiunto ordine: {request}")
        return order_management_pb2.StringMessage(value=str(id))

    # unary RPC
    def getOrder(self, request, context):
        return self.orders_dict.get(request.value, order_management_pb2.Order())

    # RPC with server streaming
    def searchOrders(self, request, context):
        orders = [order for id, order in self.orders_dict.items() if request.value in order.items]
        for order in orders:
            yield order
    
    # RPC with Bi-di streaming
    def processOrders(self, request_iterator, context):
        location_dict = {}

        # è la forma più compatta ed elegante
        ##################################################################
        for order in request_iterator:
            location_dict.setdefault(order.destination, []).append(order)
        ##################################################################

        # di
        ##################################################################
        #if order.destination not in location_dict:
        #    location_dict[order.destination] = [order]
        #else:
        #    location_dict[order.destination].append(order)
        ##################################################################

        STATUS = "PROCESSED"
        
        for location, orders in location_dict.items():
            logging.info(f"Creando spedizione per {location} ({len(orders)} ordini)")
            id = str(random.randint(1,600))
            shipment = order_management_pb2.CombinedShipment(id=id, status=STATUS, orders=orders)
            yield shipment


def main():
    logging.basicConfig(format="[SERVER] - %(message)s", level=logging.INFO)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_management_pb2_grpc.add_OrderManagementServicer_to_server(OrderManagementServicer(), server)

    port = server.add_insecure_port("localhost:0")
    logging.info(f"In ascolto sulla porta: {port}")

    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    main()