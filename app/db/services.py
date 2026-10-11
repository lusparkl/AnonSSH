from uuid import uuid4

from sqlalchemy import select

from app.db.models import Message, User
from app.db.setup import SessionLocal, setup_database


setup_database()


def create_user() -> str:
    user_id = "anonymous-" + uuid4().hex[:4]

    with SessionLocal() as session:
        user = User(id=user_id)
        session.add(user)
        session.commit()

    return user_id


def send_message(user_id: str, text: str) -> None:
    with SessionLocal() as session:
        message = Message(author_id=user_id, text=text)
        session.add(message)
        session.commit()


def get_messages() -> list:
    with SessionLocal() as session:
        statement = select(Message).order_by(Message.created.desc()).limit(100)
        return list(session.scalars(statement).all())


def search_messages(query: str) -> list:
    with SessionLocal() as session:
        statement = select(Message).where(Message.text.ilike(f"%{query}%")).order_by(Message.created.desc()).limit(100)
        return list(session.scalars(statement).all())
