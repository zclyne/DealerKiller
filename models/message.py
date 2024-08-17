from dataclasses import dataclass

from openai.types.chat import ChatCompletionUserMessageParam

MESSAGE_ROLE_SYSTEM = "system"
MESSAGE_ROLE_ASSISTANT = "assistant"
MESSAGE_ROLE_USER = "user"


@dataclass
class Message:
    """A `Message` represents a single message that is either sent by the user or by the LLM
    It is a simplified version of `openai.types.chat.ChatCompletionMessageParam`
    """

    id: int = 0
    """A unique identifier of this message."""

    conversation_id: int
    """ID of the conversation that the message belongs to."""

    role: str
    """The role of the messages author, can be either `MESSAGE_ROLE_SYSTEM`, `MESSAGE_ROLE_ASSISTANT` or `MESSAGE_ROLE_USER`."""

    content: str
    """The content of the message."""

    def to_ChatCompletionUserMessageParam(self) -> ChatCompletionUserMessageParam:
        return ChatCompletionUserMessageParam(content=self.content, role=self.role)
