from time import sleep

import stomp
import json
import logging
import argparse

FILENAME = "bw.txt"

class MyListener(stomp.ConnectionListener):
    def __init__(self, print_type):
        super().__init__
        self.print_type = print_type
    
    def on_message(self, frame):
        msg = json.loads(frame.body)

        if msg["tipo"] == self.print_type:
            with open(FILENAME, "a") as f:
                f.write(msg["pathFile"] + "\n")
            
            logging.info(f"Scritto {msg["pathFile"]}")
        else:
            logging.warning(f"Impossibile scrivere {msg["pathFile"]} - tipo di stampa: {msg["tipo"]} non supportato")


def main():
    logging.basicConfig(
        format="[BW PRINTER] - %(message)s",
        level = logging.INFO
        )
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type_to_print", type=str, help="Type to print, gs or bw")
    args = parser.parse_args()

    type_to_print = args.type_to_print.lower().strip()

    if type_to_print not in ["bw", "gs"]:
        raise ValueError("Tipo di stmpa non consentito!")
    
    with stomp.Connection([("localhost", 61613)]) as conn:
        conn.set_listener("", MyListener(type_to_print))
        conn.connect(wait=True)
        conn.subscribe("/queue/bw", id=2)

        while True:
            sleep(1)

if __name__ == "__main__":
    main()  