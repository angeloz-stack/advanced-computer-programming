from time import sleep
import stomp
import json
import logging
import argparse

FILENAME = "color.txt"

class MyListener(stomp.ConnectionListener):
    def __init__(self, file_ext):
        super().__init__
        self.file_ext = file_ext
    
    def on_message(self, frame):
        msg = json.loads(frame.body)

        if msg["pathFile"].endswith(self.file_ext):
            with open(FILENAME, "a") as f:
                f.write(msg["pathFile"] + "\n")
            logging.info(f"Scritto {msg["pathFile"]}")
        else:
            logging.warning(f"Impossibile scrivere {msg["pathFile"]} - ext non supportata")


def main():
    logging.basicConfig(
        format="[BW PRINTER] - %(message)s",
        level = logging.INFO
        )
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--ext", type=str, help="File ext, txt or doc")
    args = parser.parse_args()

    ext = args.ext.lower().strip()

    if ext not in ["txt", "doc"]:
        raise ValueError("Tipo di stmpa non consentito!")
    
    with stomp.Connection([("localhost", 61613)]) as conn:
        conn.set_listener("", MyListener(ext))
        conn.connect(wait=True)
        conn.subscribe("/queue/color", id=3)

        while True:
            sleep(1)

if __name__ == "__main__":
    main()