from os import getenv

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


load_dotenv()
url = getenv("DB_LINK", "sqlite:///anonshh.db")

if url.startswith("postgresql://"):
    url = url.replace("postgresql://", "postgresql+psycopg://", 1)

engine = create_engine(url)

SessionLocal = sessionmaker(
    bind=engine,
    expire_on_commit=False
)


def setup_database():
    from app.db.models import Base

    Base.metadata.create_all(engine)
