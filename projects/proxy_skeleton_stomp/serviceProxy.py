from Iservice import Iservice
import socket
import json

# questo è il Proxy che il dispatcher usa per
# comunciare con il server (o meglio, con il)
# suo skeleton.

class serviceProxy(Iservice):

    def __init__(self, port):
        self.port = port
        
    def preleva(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.port))

            data = {"metodo": "preleva", "id": None}
            msg = json.dumps(data)

            s.send(msg.encode("utf-8"))

            response = s.recv(1024).decode("utf-8")

            return int(response)


    def deposita(self, id_articolo):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", self.port))

            data = {"metodo": "deposita", "id": id_articolo}
            msg = json.dumps(data)

            s.send(msg.encode("utf-8"))
            
            response = s.recv(1024).decode("utf-8")

            return response