import stomp
import logging
import requests
import json
from time import sleep

ADDRESS = "http://127.0.0.1:2222"

HANDLERS = {
    "CREATE" : ("/bookings", "POST"),
    "UPDATE" : ("/bookings/update", "PUT")
}


class MyListener(stomp.ConnectionListener):
    def __init__(self, conn: stomp.Connection):
        self.connection = conn

    def on_message(self, frame):
        msg = json.loads(frame.body) # dict della richiesta
        logging.info(f"Ricevuto : {msg}")

        url, method = HANDLERS[msg["tipo_richiesta"]]
        del msg["tipo_richiesta"]
        response = requests.request(method, ADDRESS + url, json=msg)

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError:
            logging.debug(f"Error from server: {response.status_code} - {response.text}")
        else:
            logging.debug(f"OK from server: {response.status_code} - {response.text}")
    
        self.connection.send("/topic/response", json.dumps({"text" : response.text, "code": response.status_code}))


def main():
    logging.basicConfig(
        format="[BOOKING MANAGER] - %(threadName)s - %(message)s",
        level=logging.INFO
    )

    with stomp.Connection([("localhost", 61613)]) as conn:
        conn.set_listener("", MyListener(conn))
        conn.connect(wait=True)

        conn.subscribe("/topic/request", id=1)

        while True:
            sleep(1)

if __name__ == "__main__":
    main()