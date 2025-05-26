from abc import ABC, abstractmethod 


class Command(ABC):
    """
    Base class for creating commands
    """

    @abstractmethod
    def execute(self):
        pass
