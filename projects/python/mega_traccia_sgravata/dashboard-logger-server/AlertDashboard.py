import logging
import multiprocessing as mp
import stomp
import requests
from time import sleep


ADDRESS = "http://localhost:5001/alert"

def proc_func(reading: str):
    print(f"[DASHBOARD (process)] - Ricevuto {reading}")

    with open("alerts.txt", "a") as f:
        f.write(reading + "\n")

    # stringa ricevuta: zone-meterId-reading
    params = reading.split("-")

    data = {
        "zone": params[0],
        "meterId": int(params[1]),
        "reading": int(params[2])
    }

    response = requests.post(ADDRESS, json=data)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        print(f"[DASHBOARD (process)] - ERROR dal server {response.status_code} - {response.text}")
    else:
        print(f"[DASHBOARD (process)] - OK dal server {response.status_code} - {response.text}")

class AlertListener(stomp.ConnectionListener):
    def on_message(self, frame):

        reading = frame.body
        logging.info(f"Ricevuto {reading}")
        logging.info("Avvio processo...")

        p = mp.Process(target=proc_func, args = (reading,))
        p.start()

def main():

    logging.basicConfig(
        format = "[ALERT DASHBOARD] %(levelname)s - %(message)s",
        level = logging.INFO
    )

    with stomp.Connection([("localhost", 61613)]) as conn:
        conn.set_listener("", AlertListener())
        conn.connect(wait=True)
        conn.subscribe("/topic/alert", id = 1)

        while True:
            sleep(1)

if __name__ == "__main__":
    main()