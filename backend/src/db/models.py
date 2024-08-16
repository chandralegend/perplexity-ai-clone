"""Models for the database."""

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Chat(Base):
    """Chat model."""
    __tablename__ = "chats"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=True)
    description = Column(String, index=True, nullable=True)
    
    messages = relationship("Message", back_populates="chat")

class Message(Base):
    """Message model."""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String, index=True)
    related_sources = Column(String, index=True)
    answer = Column(String, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    
    chat = relationship("Chat", back_populates="messages")