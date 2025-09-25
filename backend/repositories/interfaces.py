from abc import ABC, abstractmethod

class IUserRepository(ABC):
    @abstractmethod
    def create(self, user_data: dict):
        pass
    
    @abstractmethod
    def get_by_id(self, user_id: int):
        pass
    
    @abstractmethod
    def get_by_email(self, email: str):
        pass

class IArticleRepository(ABC):
    @abstractmethod
    def create(self, article_data: dict):
        pass
    
    @abstractmethod
    def get_by_id(self, article_id: int):
        pass
    
    @abstractmethod
    def get_all(self, page: int = 1, per_page: int = 10, filters: dict = None):
        pass

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
