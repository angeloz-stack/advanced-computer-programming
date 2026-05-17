import argparse
import order_management_pb2
import order_management_pb2_grpc
import grpc
import logging

# Usiamo yield per trasformare questa funzione in un generatore.
# processOrders è una chiamata stream-stream: il client deve fornire
# un iteratore di ordini, non una lista. Con yield, gli ordini vengono
# prodotti uno alla volta e passati direttamente allo stream gRPC,
# senza caricare tutto in memoria in anticipo.
#######################################################################
def generate_orders_for_processing():
    ord1 = order_management_pb2.Order(
        id='104', price=2332,
        items=['Item - A', 'Item - B'],  
        description='Updated desc', 
        destination='San Jose, CA')
    
    ord2 = order_management_pb2.Order(
        id='105', price=3000, 
        description='Updated desc', 
        destination='San Francisco, CA')
    
    ord3 = order_management_pb2.Order(
        id='106', price=2560, 
        description='Updated desc', 
        destination='San Francisco, CA')
    
    ord4 = order_management_pb2.Order(
        id='107', price=2560, 
        description='Updated desc', 
        destination='Mountain View, CA')
    
    list = []
    list.append(ord1)
    list.append(ord2)
    list.append(ord3)
    list.append(ord4)

    for processing_orders in list:
        yield processing_orders
#######################################################################

def main():

    logging.basicConfig(format="[CLIENT] - %(message)s", level=logging.INFO)

    
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, help="Port")
    args = parser.parse_args()
    
    address = f"localhost:{args.port}"

    with grpc.insecure_channel(address) as channel:

        stub = order_management_pb2_grpc.OrderManagementStub(channel)

        # definisco i 5 ordini

        orders = []

        orders.append(order_management_pb2.Order(price=2450.50,
                                            items=['Item - A', 'Item - B', 'Item - C'],
                                            description='This is a Sample order - 1 : description.', 
                                            destination='San Jose, CA'))

        orders.append(order_management_pb2.Order(price=1000, 
                                            items=['Item - A', 'Item - B'], 
                                            description='Sample order description.',
                                            destination='Naples'))
        
        orders.append(order_management_pb2.Order(price=1000, 
                                            items=['Item - C'], 
                                            description='Sample order description.',
                                            destination='Rome'))

        orders.append(order_management_pb2.Order(price=1000, 
                                            items=['Item - A', 'Item - E'], 
                                            description='Sample order description.',
                                            destination='Milan'))
    
        orders.append(order_management_pb2.Order(price=1000, 
                                            items=['Item - F', 'Item - G'], 
                                            description='Sample order description.'))

        for order in orders:
            id = stub.addOrder(order)
            logging.info(f"Ricevuto id {id}")

            # verifica dell’aggiunta dell’ordine

            logging.info(f"Verifico ordine con id {id}")

            return_order = stub.getOrder(id)

            # Per stampare le info dell'ordine ritornato da getOrder hai due strade
            # tenendo bene in mente che l'ogetto è già deserializzato:
            # 1. accedi a ogni campo, e printi (return_order.price, return_order.description...)
            # 2. gli oggetti protobuf hanno un metodo built-in __str__ che permette di stampare
            # tutti i campi già in un formato human readable
            #####################################################
            logging.info(f"[Info ordine {id}] - {return_order}")   
            #####################################################

        # richiesto una lista di ordini che contengono l' Item - A

        item_to_find = "Item - A"
        logging.info(f"Search result for {item_to_find}:")
        for order_search_result in stub.searchOrders(order_management_pb2.StringMessage(value = item_to_find)):
            logging.info(order_search_result)


        order_iterator = generate_orders_for_processing()
        for shipment in stub.processOrders(order_iterator):
            logging.info(f"Shipment: {shipment}")

if __name__ == "__main__":
    main()        