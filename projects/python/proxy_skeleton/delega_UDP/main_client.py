from threading import Thread
import argparse
import random
import time
import logging
from Proxy import Proxy
from config import ARTICLES, REQUESTS_PER_THREAD

def thd_func(ip: str, port: int, metodo: str):

    p = Proxy(ip, port)
    
    for _ in range(REQUESTS_PER_THREAD):

        t = random.randint(2,4)

        time.sleep(t)

        articolo = random.choice(ARTICLES)

        if metodo == "deposita":

            # serve articolo e id
            id = random.randint(1,100)

            if p.deposita(articolo, id):
                logging.info(f"Deposito avvenuto - articolo: {articolo}, id: {id}")
            else:
                logging.info(f"Errore in deposito")

        elif metodo == "preleva":
            id = p.preleva(articolo)

            if id != -1:
                logging.info(f"Prelievo avvenuto - articolo: {articolo}, id: {id}")
            else:
                logging.info(f"Errore in prelievo")
    

def main():

    logging.basicConfig(
        format = "CLIENT [%(threadName)-15s] %(levelname)-8s %(message)s",
        level = logging.INFO,
        handlers = [logging.StreamHandler()]
    )

    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="localhost", help="ip dest")
    parser.add_argument("-p", "--port", type=int, help="porta")
    parser.add_argument("-m", "--metodo", type=str, help="metodo da chiamare")
    parser.add_argument("-n", "--num_threads", type=int, help="numero di thread clienti")
    args = parser.parse_args()

    threads = []

    for i in range(args.num_threads):

        t = Thread(target=thd_func, args=(args.ip, args.port, args.metodo,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
