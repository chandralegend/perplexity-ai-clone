"""CRUD operations for the database."""

import uuid

from sqlalchemy.orm import Session

from . import models, schemas

def get_chat(db: Session, chat_id: int) -> list[models.Message]:
    """Get a chat by id."""
    messages = db.query(models.Message).filter(models.Message.chat_id == chat_id).all()
    return messages

def get_chats(db: Session) -> list[models.Chat]:
    """Get all chats."""
    return db.query(models.Chat).all()

def create_chat(db: Session) -> models.Chat:
    """Create a chat."""
    chat_id = str(uuid.uuid4())
    chat = models.Chat(id=chat_id)
    db.add(chat)
    db.commit()
    db.refresh(chat)
    return chat

def delete_chat(db: Session, chat_id: int) -> None:
    """Delete a chat by id."""
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    db.delete(chat)
    db.commit()
    messages = db.query(models.Message).filter(models.Message.chat_id == chat_id).all()
    for message in messages:
        db.delete(message)
    db.commit()

def create_message(db: Session, message: schemas.Message, chat_id: int) -> models.Message:
    """Create a message."""
    db_message = models.Message(**message.dict(), chat_id=chat_id)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def delete_message(db: Session, message_id: int) -> None:
    """Delete a message by id."""
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    db.delete(message)
    db.commit()

def update_message(db: Session, message_id: int, message: schemas.Message) -> models.Message:
    """Update a message by id."""
    db_message = db.query(models.Message).filter(models.Message.id == message_id).first()
    db_message.question = message.question
    db_message.related_sources = message.related_sources
    db_message.answer = message.answer
    db.commit()
    db.refresh(db_message)
    return db_message