from ServerImpl import ServerImpl
import argparse
from config import ARTICLES, QUEUE_SIZE
import logging

def main():

    logging.basicConfig(
        format = "SERVER [%(threadName)-15s] %(levelname)-8s %(message)s",
        level = logging.INFO,
        handlers = [logging.StreamHandler()]
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, help="Server ip, usa 0.0.0.0 per ascoltare su tutte interfacce")
    parser.add_argument("-p", "--port", type=int, help="porta, usa 0 per prima disponibile")
    args = parser.parse_args()

    s = ServerImpl(args.ip, args.port, QUEUE_SIZE, ARTICLES)
    s.runSkeleton()

if __name__ == "__main__":
    main()