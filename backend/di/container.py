from typing import Dict, Any, TypeVar, Type
from database import IDatabaseConnection
from database.connections import SQLiteDatabaseConnection, PostgreSQLDatabaseConnection

T = TypeVar("T")


class DIContainer:
    def __init__(self):
        self._services: Dict[str, Any] = {}
        self._singletons: Dict[str, Any] = {}

    def register_instance(self, interface: Type[T], instance: T):
        """Реєструє конкретний екземпляр"""
        self._singletons[interface.__name__] = instance

    def resolve(self, interface: Type[T]) -> T:
        """Розв'язує залежність"""
        interface_name = interface.__name__

        if interface_name in self._singletons:
            return self._singletons[interface_name]

        raise ValueError(f"Service {interface_name} not registered")


container = DIContainer()


def configure_dependencies(app_config):
    """Конфігурація залежностей"""

    # Отримуємо значення з конфігурації Flask
    database_type = getattr(app_config, "DATABASE_TYPE", "sqlite")
    database_url = getattr(app_config, "DATABASE_URL", "sqlite:///news.db")

    # Database connection
    if database_type.lower() == "sqlite":
        db_connection = SQLiteDatabaseConnection(database_url)
    elif database_type.lower() == "postgresql":
        db_connection = PostgreSQLDatabaseConnection(database_url)
    else:
        raise ValueError(f"Unsupported database type: {database_type}")

    container.register_instance(IDatabaseConnection, db_connection)

    return container
