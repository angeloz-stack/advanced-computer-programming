from time import sleep
import threading
from threading import Thread
from loguru import logger
import sys
import argparse

logger.remove()
logger.add(sink=sys.stderr,format="{level} {thread.name} {message}")

class MyThread(Thread):
    def run(self):
        logger.info("Running")
        for i in range(10):
            sleep(1)
            logger.info("Still running, Main thread is alive: {}", threading.main_thread().is_alive())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--daemon", action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    
    m = MyThread(daemon=args.daemon)
    m.start()

    if m.is_alive():
        return # <-- Forzo la terminazione
    
if __name__ == "__main__":

    main()
    logger.info("Is alive {}", threading.main_thread().is_alive())