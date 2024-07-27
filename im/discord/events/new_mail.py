import asyncio
import logging

from event.dispatcher import default_event_dispatcher
from event.error import WrongEventTypeError
from event.event import Event
from event.handler import EventHandler
from im.discord.client import get_client
from im.discord.message_type import MessageType

NEW_MAIL_EVENT = "new_mail"

logger = logging.getLogger(__name__)


class NewMailEvent(Event):
    def __init__(
        self, channel_id: int, sender: str, receiver: str, content: str
    ) -> None:
        # TODO: support attachment
        self.type: str = NEW_MAIL_EVENT
        self.channel_id = channel_id
        self.sender: str = sender
        self.receiver: str = receiver
        self.content: str = content

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, sender={self.sender!r}, receiver={self.receiver!r}, content={self.content!r})"


class NewMailEventHandler(EventHandler):
    async def handle(self, event: Event):
        if not isinstance(event, NewMailEvent):
            raise WrongEventTypeError(
                f"event {event} is not instance of {NewMailEvent.__name__}"
            )
        logger.info(f"handling new mail event {event}")
        message = f"sender: {event.sender}, content: {event.content}"
        await get_client().send_message(
            channel_id=event.channel_id,
            content=message,
            message_type=MessageType.MailContent,
        )


asyncio.run(default_event_dispatcher.register(NEW_MAIL_EVENT, NewMailEventHandler()))
