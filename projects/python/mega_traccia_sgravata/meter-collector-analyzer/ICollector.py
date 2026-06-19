from abc import ABC, abstractmethod

class ICollector(ABC):
    @abstractmethod
    def submit(self, meterId: int, zone: str, reading: int) -> None:
        raise NotImplementedError