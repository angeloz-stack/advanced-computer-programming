import stomp
import logging
import argparse
from time import sleep
from Checker import ALERT

FILENAME = "alerts.txt"

class AlertsListener(stomp.ConnectionListener):
    def on_message(self, frame):
        temp = frame.body
        logging.info(f"Ricevuto {temp}")

        with open(FILENAME, "a") as f:
            f.write(temp + "\n")
        

def main():
    logging.basicConfig(
        format="[AlertDashboard] - [%(threadName)s] - %(message)s",
        level=logging.INFO
    )

    with stomp.Connection([("localhost", 61613)]) as conn:
        conn.connect(wait=True)
        conn.set_listener("", AlertsListener())

        conn.subscribe(ALERT, id=1)

        while True:
            sleep(1)

if __name__ == "__main__":
    main()