from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, String

from .base import Base
from .message import Message


class Conversation(Base):
    """A `Conversation` represents an entire conversation between the user and the LLM for a single dealer

    It includes the history of every prompt sent by the user to the LLM
    and the response generated  by the LLM
    """

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    """A unique identifier of the conversation."""

    dealer_email: Mapped[str] = mapped_column(String(40), unique=True)
    """The email address of the dealer for this conversation."""

    messages: Mapped[list[Message]] = relationship()
    """The message history."""

    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    """the datetime when the conversation is created."""

    def __repr__(self) -> str:
        return f"Conversation(id={self.id!r}, dealer_email={self.dealer_email!r}, messages={self.messages!r}, created={self.created!r})"
