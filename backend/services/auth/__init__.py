from abc import ABC
from typing import Any, Dict


class TokenFactory(ABC):
    def create_token(self, entity, **kwargs) -> Dict[str, Any]:
        pass
    
    def get_factory_type(self) -> str:
        pass

class AuthStrategy:
    def __init__(self, repo):
        self.repo = repo
        
    def register(self, email: str, password: str):
        pass

    def authenticate(self, email: str, password: str):
        pass

    def refresh(self, refresh_token: str):
        pass

    def verify(self, token: str):
        pass


class AuthServiceContext:
    def __init__(self, strategy: AuthStrategy):
        self._state = strategy

    @property
    def strategy(self):
        return self._state

    @strategy.setter
    def strategy(self, strategy: AuthStrategy) -> None:
        self._strategy = strategy
