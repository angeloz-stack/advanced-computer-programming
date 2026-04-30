'''
Nel client dobbiamo creare un canale gRPC per comunicare con il server.
Per eseguire le RPC usiamo lo stub generato nel file `helloworld_pb2_grpc.py`
'''

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

PORT = 5001

def main():

    address = f"localhost:{PORT}"
    with grpc.insecure_channel(address) as channel:
        
        # creo lo stub passandogli il canale
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        
        # invoco il servizio passandogli il messaggio serializzato
        # nota che `name` è un campo definito in `HelloRequest`
        # nel file `.proto` e anche il return è definito li
        response = stub.SayHello(helloworld_pb2.HelloRequest(name="Angelo"))

        print(f"[CLIENT] SayHello invoked Greeter and received {response.message}")

if __name__ == "__main__":
    main()
