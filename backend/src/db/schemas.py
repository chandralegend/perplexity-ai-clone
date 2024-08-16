"""Schema definitions for the database models."""

from pydantic import BaseModel

class Message(BaseModel):
    """Message schema."""
    id: int
    question: str
    related_sources: list[str]
    answer: str
    chat_id: int

    class Config:
        orm_mode = True