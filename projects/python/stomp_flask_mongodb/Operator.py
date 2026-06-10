import stomp
import logging
import argparse
import threading
import random
import json
from time import sleep

def thd_func(conn: stomp.Connection, lock: threading.Lock, message: dict):
    data = json.dumps(message)

    with lock:
        conn.send("/topic/request", data)
    
    logging.info(f"Inviato {data}")

class MyListener(stomp.ConnectionListener):
    def on_message(self, frame):
        logging.info(f"Ricevuto: {frame.body}")
    

def main():
    logging.basicConfig(
        format="[OPERATOR] - %(threadName)s - %(message)s",
        level=logging.INFO
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--operator", type=str, help="operator")
    args = parser.parse_args()

    lock = threading.Lock()

    with stomp.Connection([("localhost", 61613)]) as conn:
        
        conn.set_listener("", MyListener())
        conn.connect(wait=True)
        conn.subscribe("/topic/response", id=1)

        threads=[]

        for i in range(6):
            # i primi 4 mandato CREATE, GLI ULTIMI DUE MANDANO UPDATE
            if i<=3:
                message = {
                    "tipo_richiesta": "CREATE",
                    "client": "ILoveTravel",
                    "hotel": "Vesuvio", 
                    "operator": args.operator, 
                    "nights": random.randint(2, 10), 
                    "people": random.randint(1, 5), 
                    "cost": random.randint(100, 500)}

            else:
                message = {
                    "tipo_richiesta": "UPDATE",
                    "operator" : args.operator,
                    "nights": random.randint(2, 10),
                    "discount": random.randint(10, 200)
                }

            t = threading.Thread(target=thd_func, args=(conn, lock, message))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        while True:
            sleep(1)


if __name__ == "__main__":
    main()