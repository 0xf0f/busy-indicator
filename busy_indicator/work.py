from abc import ABC, abstractmethod


class Work(ABC):
    def started(self):
        pass

    def finished(self):
        pass

    @abstractmethod
    def iterate(self):
        pass

    @abstractmethod
    def complete(self) -> bool:
        pass

    @abstractmethod
    def status(self) -> str:
        pass

    @abstractmethod
    def progress(self) -> str:
        pass

