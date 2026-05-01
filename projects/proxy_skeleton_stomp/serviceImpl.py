from serviceSkeleton import serviceSkeleton
import multiprocessing as mp
import logging

QUEUE_SIZE = 5

class serviceImpl(serviceSkeleton):
    def __init__(self):
        self.queue = mp.Queue(QUEUE_SIZE)

    def preleva(self):
        id = self.queue.get()

        logging.info(f"Prelevato id: {id}")
        return id
    
    def deposita(self, id_articolo):
        
        self.queue.put(id_articolo)
        logging.info(f"Depositato id: {id_articolo}")

        return "deposited"
    
