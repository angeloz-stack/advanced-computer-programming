'''
Nel server dobbiamo implementare l'interfaccia del servizio dalla sua definizione,
che si trova in `helloworld_pb2_grpc.py`.
'''

import grpc
from concurrent import futures
import helloworld_pb2_grpc
import helloworld_pb2

PORT = 5001

# La classe Greeter eredita da GreeterServicer, e in questo caso implementiamo
# il metodo SayHello

class Greeter(helloworld_pb2_grpc.GreeterServicer):
    # SayHello è la nostra RPC, il client la invocherà con uno stub
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f"hello, {request.name}!")


def serve():
    
    # al server passo un pool di thread per poter parallelizzare le richieste
    # nota che comunque è soggetto alla problematica del GIL
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # aggiugiamo al server l'istanza del Greeter
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    address = f"[::]:{PORT}" # e.g. [::]:5501 
    server.add_insecure_port(address)

    server.start()

    print(f"[SERVER] Listening on {address}")

    server.wait_for_termination()

if __name__ == "__main__":
    serve()