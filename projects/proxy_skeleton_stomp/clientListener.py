import stomp
import logging

class clientListener(stomp.ConnectionListener):
    def on_message(self, frame):
        logging.info(f"Ricevuto {frame.body}")