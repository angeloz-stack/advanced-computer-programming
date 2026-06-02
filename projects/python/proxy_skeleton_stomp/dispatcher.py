from stomp import logging
import stomp
from dispatcherListener import dispatcherListener
import time
import logging
import argparse

# Questo è il dispatcher. Si mette in ascolto
# dei messagi che arrivano sulla coda richiesta
# NOTA: il dispatcher ha anche il ruolo di inoltrare
# i messaggi al server; questo scopo viene implementato
# direttamente nel listener. Praticamente questo main
# ha il solo scopo di eseguire il listener stesso

def main():

    logging.basicConfig(
        level = logging.INFO,
        format = "[LISTENER] %(processName)s - %(levelname)s - %(message)s",
        force=True
    )


    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int)
    args = parser.parse_args()

    conn = stomp.Connection([("localhost", 61613)])
    conn.set_listener('', dispatcherListener(args.port))

    conn.connect(wait=True)
    conn.subscribe(destination="/queue/richiesta", id=1)

    # manteniamo il programma
    # vivo per mantenere in
    # esecuzione il listener
    #########################
    while True:
        time.sleep(60)
    #########################

if __name__ == "__main__":
    main()