import stomp
from clientListener import clientListener
import time
import random
import logging
import json

N_REQS = 10
METODI = ["deposita", "preleva"]


def main():

    logging.basicConfig(
        format = "[CLIENT] %(processName)s %(levelname)s %(message)s",
        level = logging.INFO,
        handlers = [logging.StreamHandler()]
    )

    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener('', clientListener())
    conn.connect(wait=True)
    conn.subscribe(destination="(/queue/risposta)", id=1)

    for i in range(N_REQS):
        
        metodo = random.choice(METODI)
        id = None

        if metodo == "deposita":
            id = random.randint(1,100)

        data = {"metodo" : metodo, "id": id}
        logging.info(f"Invio {data}")
        message = json.dumps(data)

        conn.send("/queue/richiesta", message)

    while True:
        time.sleep(60)

    conn.disconnect()

if __name__ == "__main__":
    main()