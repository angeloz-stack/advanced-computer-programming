import stomp
import json
import config
import random
import logging
from time import sleep

'''
{
"metodo" : str
"id_articolo" : int
"prodotto" : str
}
'''

class ClientListener(stomp.ConnectionListener):
    def on_message(self, frame):
        logging.info(f"Riceuvto : {frame.body}")

def main():

    logging.basicConfig(format="[CLIENT] - %(message)s", level=logging.INFO)

    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener("", ClientListener())
    conn.connect(wait=True)
    conn.subscribe(config.QUEUE_RESPONSES, id = 1)

    # deposita

    for _ in range(10):
        request = {
            "metodo": "deposita",
            "id_articolo": random.randint(1,100),
            "prodotto": random.choice(config.PRODOTTI)
        }

        conn.send(config.QUEUE_REQUESTS, json.dumps(request))

    # preleva

    for _ in range(5):
        request = {
            "metodo": "preleva",
            "id_articolo": "",
            "prodotto": ""
        }

        conn.send(config.QUEUE_REQUESTS, json.dumps(request))

    request = {
            "metodo": "svuota",
            "id_articolo": "",
            "prodotto": ""
        }

    conn.send(config.QUEUE_REQUESTS, json.dumps(request))

    while True:
        sleep(1)
    

if __name__ == "__main__":
    main()