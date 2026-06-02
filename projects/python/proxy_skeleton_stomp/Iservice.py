from abc import ABC, abstractmethod

# Questa è l'interfaccia che usiamo per
# implementare il paradigma proxy skeleton
# Dato che lo facciamo per ereditarietà
# da questa ereditano il proxy e lo skeleton
# e dallo skeleton l'impl del server
##########################################
class Iservice(ABC):
    @abstractmethod
    def preleva(self) -> int:
        raise NotImplementedError
    
    @abstractmethod
    def deposita(self, id_articolo: int):
        raise NotImplementedError
##########################################