import asyncio
import logging

from event.dispatcher import default_event_dispatcher
from event.error import WrongEventTypeError
from event.event import Event
from event.handler import EventHandler
from im.discord.client import get_client
from im.discord.message_type import MessageType

GENERATED_RESPONSE_EVENT = "generated_response"

logger = logging.getLogger(__name__)


class GeneratedResponseEvent(Event):
    def __init__(self, channel_id: int, content: str) -> None:
        # TODO: support attachment
        self.type = GENERATED_RESPONSE_EVENT
        self.channel_id = channel_id
        self.content: str = content

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(type={self.type!r}, content={self.content!r})"
        )


class GeneratedResponseEventHandler(EventHandler):
    async def handle(self, event: Event):
        if not isinstance(event, GeneratedResponseEvent):
            raise WrongEventTypeError(
                f"event {event} is not instance of {GeneratedResponseEvent.__name__}"
            )
        logger.info(f"handling generated response event {event}")
        message = f"content: {event.content}"
        await get_client().send_message(
            channel_id=event.channel_id,
            content=message,
            message_type=MessageType.MailResponse,
        )


asyncio.run(
    default_event_dispatcher.register(
        GENERATED_RESPONSE_EVENT, GeneratedResponseEventHandler()
    )
)
