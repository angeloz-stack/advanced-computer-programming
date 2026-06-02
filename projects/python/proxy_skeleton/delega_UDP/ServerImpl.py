from threading import Lock, Condition
import logging

from IMagazzino import IMagazzino

class ServerImpl(IMagazzino):

    """
    Il server effettivo che implementa i servizi, ed eredita la comunicazione dallo
    skeleton.    
    """

    def __init__(self, queue_size, articoli: list):
        self.queue_size = queue_size
        self.articoli = articoli
        self.risorse = {}

        for art in self.articoli:
            l = Lock()

            self.risorse[art] = {
                "queue" : [],
                "cv_prod" : Condition(lock = l),
                "cv_cons" : Condition(lock = l),
                "filename": f"{art}_logs.txt"
            }

    # Funzioni helper
    ##############################################
    def an_item_is_available(self, queue):
        return not (len(queue) == 0)

    def a_space_is_available(self, queue):
        return not (len(queue) == self.queue_size)
    ##############################################

    def deposita(self, articolo: str, id: int) -> bool:

        success = True

        if articolo not in self.articoli:
            logging.warning(f"Articolo non riconosciuto")
            return not success

        assets = self.risorse[articolo]

        with assets["cv_prod"]:

            assets["cv_prod"].wait_for(lambda: self.a_space_is_available(assets["queue"]))
            assets["queue"].append(id) # aggiungo all'ultimo posto

            logging.info(f"Aggiunto {articolo} con id: {id}")

            assets["cv_cons"].notify()

        return success

    def preleva(self, articolo: str) -> int:

        id = -1

        if articolo not in self.articoli:
            logging.warning(f"Articolo non riconosciuto")
            return id

        assets = self.risorse[articolo]

        with assets["cv_cons"]:
            
            assets["cv_cons"].wait_for(lambda: self.an_item_is_available(assets["queue"]))
            id = assets["queue"].pop(0) # prendo il primo

            logging.info(f"Prelevato articolo {articolo} con id: {id}")

            assets["cv_prod"].notify()

        return id
        