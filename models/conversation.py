from dataclasses import dataclass

from .message import Message


@dataclass
class Conversation:
    """A `Conversation` represents an entire conversation between the user and the LLM for a single dealer

    It includes the history of every prompt sent by the user to the LLM
    and the response generated  by the LLM
    """

    id: int
    """A unique identifier of the conversation."""

    dealer_address: str
    """The email address of the dealer for this conversation."""
    messages: list[Message]
    """The message history."""
