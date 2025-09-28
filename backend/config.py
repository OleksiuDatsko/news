import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


class Config:
    # Flask settings
    SECRET_KEY = os.environ.get("SECRET_KEY", "your-secret-key-here")

    # Database settings
    DATABASE_TYPE = os.environ.get("DATABASE_TYPE", "sqlite")
    DATABASE_URL = os.environ.get("DATABASE_URL", f"sqlite:///{BASE_DIR}/news.db")

    # JWT settings
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-string")
    JWT_ACCESS_TOKEN_EXPIRES = 3600


class DefaultConfig(Config):
    DEBUG = True
    DATABASE_TYPE = "sqlite"
    DATABASE_URL = f"sqlite:///{BASE_DIR}/news.db"


class TestingConfig(Config):
    TESTING = True
    DATABASE_TYPE = "sqlite"
    DATABASE_URL = "sqlite:///:memory:"


config = {"testing": TestingConfig, "default": DefaultConfig}
