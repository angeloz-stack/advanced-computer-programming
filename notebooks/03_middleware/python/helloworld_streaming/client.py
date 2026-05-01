import grpc
import helloworld_pb2
import helloworld_pb2_grpc

PORT = 5001

def generate_requests():

	names = ['Raf', 'Gigi', 'Pippo', 'Pippozzo']
	for name_to_send in names:
		yield helloworld_pb2.HelloRequest(name=name_to_send)

def run():
	# NOTE(gRPC Python Team): .close() is possible on a channel and should be
	# used in circumstances in which the with statement does not fit the needs
	# of the code.
	print("Will try to greet world ...")

	# creo un canale verso il server RPC
	with grpc.insecure_channel(f"localhost:{PORT}") as channel: 
		
		# creo uno stub (GreeterStub, ovvero ${NOMESERVIZIO}Stub) per invocare tutti i metodi implementati nel servizio
		stub = helloworld_pb2_grpc.GreeterStub(channel)
		
		# Server streaming
		for response in stub.SayHello_v1(helloworld_pb2.HelloRequest(name="you")):
			print("[CLIENT] SayHello invoked Greeter client received: " + response.message)


		# Client streaming
		response = stub.SayHello_v2(generate_requests())
		print("[CLIENT] SayHello invoked Greeter client received: " + response.message)

		# Bi-directional streaming
		for response in stub.SayHello_v3(generate_requests()):
			print("[CLIENT] SayHello invoked Greeter client received: " + response.message)
		
if __name__ == "__main__":
	run()