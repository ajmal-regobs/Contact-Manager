import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Contact Manager DB
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_DB = os.getenv("POSTGRES_DB", "contact_manager")

DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
    f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Logs DB
LOGS_DB_USER = os.getenv("LOGS_DB_USER", "postgres")
LOGS_DB_PASSWORD = os.getenv("LOGS_DB_PASSWORD", "postgres")
LOGS_DB_HOST = os.getenv("LOGS_DB_HOST", "localhost")
LOGS_DB_PORT = os.getenv("LOGS_DB_PORT", "5432")
LOGS_DB_NAME = os.getenv("LOGS_DB_NAME", "logs_db")

LOGS_DATABASE_URL = (
    f"postgresql://{LOGS_DB_USER}:{LOGS_DB_PASSWORD}"
    f"@{LOGS_DB_HOST}:{LOGS_DB_PORT}/{LOGS_DB_NAME}"
)

logs_engine = create_engine(LOGS_DATABASE_URL)
LogsSessionLocal = sessionmaker(bind=logs_engine)
LogsBase = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_logs_db():
    db = LogsSessionLocal()
    try:
        yield db
    finally:
        db.close()
