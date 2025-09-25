from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from repositories.interfaces import IDatabaseConnection
from models.base import Base


class SQLiteDatabaseConnection(IDatabaseConnection):
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(
            database_url, echo=True, connect_args={"check_same_thread": False}
        )
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self) -> Session:
        return self.SessionLocal()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    @property
    def metadata(self):
        return Base.metadata
    
    @property
    def db(self):
        return self.engine


class PostgreSQLDatabaseConnection(IDatabaseConnection):
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self) -> Session:
        return self.SessionLocal()

    def create_tables(self):
        Base.metadata.create_all(bind=self.engine)

    @property
    def metadata(self):
        return Base.metadata
    
    @property
    def db(self):
        return self.engine
