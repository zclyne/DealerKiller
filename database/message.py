from datetime import datetime
from sqlalchemy import Engine, create_engine
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, String

from .base import Base

MESSAGE_ROLE_SYSTEM = "system"
MESSAGE_ROLE_ASSISTANT = "assistant"
MESSAGE_ROLE_USER = "user"


class Message(Base):
    """A `Message` represents a single message that is either sent by the user or by the LLM
    It is a simplified version of `openai.types.chat.ChatCompletionMessageParam`
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    """A unique identifier of this message."""

    conversation_id = mapped_column(ForeignKey("conversations.id"))
    """ID of the conversation that the message belongs to."""

    role: Mapped[str] = mapped_column(String(20))
    """The role of the messages author, can be either "system", "assistant" or "user"."""

    content: Mapped[str] = mapped_column(String(2048))
    """The content of the message."""

    status: Mapped[str] = mapped_column(String(10), default="draft")
    """The status of the message, either "draft" or "sent"."""

    created: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    """the datetime when the conversation is created."""

    updated: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
    """the datetime when the conversation is last updated."""

    def __repr__(self) -> str:
        return f"Message(id={self.id!r}, conversation_id={self.conversation_id!r}, role={self.role!r}, content={self.content!r}, status={self.status!r}, created={self.created!r}, updated={self.updated!r})"
