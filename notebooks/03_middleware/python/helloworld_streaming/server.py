from concurrent import futures

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

### crea una classe Greeter che implementa il servizio GreeterServicer

class Greeter(helloworld_pb2_grpc.GreeterServicer):

	# Streaming server
	def SayHello_v1(self, request, context):
		for i in range (0, 5):
			print("[server] SayHello method invoked, returning response...")
			yield helloworld_pb2.HelloReply(message="Hello, " + request.name + "! - " + str(i))


	# Streaming client
	def SayHello_v2(self, request_iterator, context):

		names = []
		for request in request_iterator:
			print("[server] SayHello method invoked, with name " + request.name)
			names.append(request.name)
		
		return helloworld_pb2.HelloReply(message="Hello, " + ' '.join(names) + "!")

	# Bi-directional streaming
	def SayHello_v3(self, request_iterator, context):

		for request in request_iterator:
			print("[server] SayHello method invoked, returning response...")
			yield helloworld_pb2.HelloReply(message="Hello, " + request.name + "!")
		


### implemento il metodo serve() che sarà invocato come prima funzione dal main

def serve():
	# definisco il porto
	port = "5001"

	# mi istanzio un oggetto server da grpc
	# ALERT: i ThreadPool sono quelli del package concurrent e non multiprocess. Alcune diff in: https://stackoverflow.com/questions/20776189/concurrent-futures-vs-multiprocessing-in-python-3
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

	# aggiungo al server l'oggetto istanza del mio servizio Greeter
	helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

	# faccio il bind al porto impostato
	# [::] è 0.0.0.0 (tutte le interfacce)
	server.add_insecure_port("[::]:" + port)

	# avvio il server
	server.start()

	print("Server started, listening on " + port)

	# attendo che il server termini
	server.wait_for_termination()


if __name__ == "__main__":
	serve()
