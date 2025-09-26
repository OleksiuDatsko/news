from abc import ABC, abstractmethod


class IDatabaseConnection(ABC):
    @abstractmethod
    def get_session(self):
        pass
    
    @abstractmethod
    def create_tables(self):
        pass

    @property
    @abstractmethod
    def metadata(self):
        pass

    @property
    @abstractmethod
    def db(self):
        pass