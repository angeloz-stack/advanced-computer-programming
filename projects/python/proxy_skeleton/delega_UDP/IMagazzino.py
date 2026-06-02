from abc import ABC, abstractmethod

class IMagazzino(ABC):

    @abstractmethod
    def deposita(self, articolo: str, id: int) -> bool:
        pass

    @abstractmethod
    def preleva(self, articolo: str) -> int:
        pass