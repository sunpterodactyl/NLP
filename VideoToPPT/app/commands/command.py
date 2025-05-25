from abc import ABC, abstractmethod 


class Command(ABC):
    """
    Base class for creating commands
    """

    def __init__(self, receiver):
        self.receiver = receiver

    @abstractmethod
    def process(self):
        pass
