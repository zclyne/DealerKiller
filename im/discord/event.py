import asyncio
import logging

import event
from config import settings
from event.dispatcher import register_handler
from event.error import WrongEventTypeError
from event.event import Event
from event.handler import EventHandler
from im.discord.client import discord
from im.discord.message_type import MessageType

GENERATED_RESPONSE_EVENT = "generated_response"
NEW_MAIL_EVENT = "new_mail"

logger = logging.getLogger(__name__)


class GeneratedResponseEvent(Event):
    def __init__(self, dealer_email: str, content: str) -> None:
        # TODO: support attachment
        self.type = GENERATED_RESPONSE_EVENT
        self.dealer_email = dealer_email
        self.content: str = content

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, dealer_email={self.dealer_email!r} content={self.content!r})"


@event.handler(event_type=GENERATED_RESPONSE_EVENT)
class GeneratedResponseEventHandler(EventHandler):
    async def handle(self, event: Event):
        if not isinstance(event, GeneratedResponseEvent):
            raise WrongEventTypeError(
                f"event {event} is not instance of {GeneratedResponseEvent.__name__}"
            )
        logger.info(f"handling generated response event {event}")
        message = f"content: {event.content}"
        await discord().send_message(
            channel_id=settings.im.discord.channel_id,
            content=message,
            message_type=MessageType.MailResponse,
        )


class NewMailEvent(Event):
    def __init__(self, sender: str, receiver: str, content: str) -> None:
        # TODO: support attachment
        self.type: str = NEW_MAIL_EVENT
        self.sender: str = sender
        self.receiver: str = receiver
        self.content: str = content

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, sender={self.sender!r}, receiver={self.receiver!r}, content={self.content!r})"


@event.handler(event_type=NEW_MAIL_EVENT)
class NewMailEventHandler(EventHandler):
    async def handle(self, event: Event):
        if not isinstance(event, NewMailEvent):
            raise WrongEventTypeError(
                f"event {event} is not instance of {NewMailEvent.__name__}"
            )
        logger.info(f"handling new mail event {event}")
        message = f"sender: {event.sender}, content: {event.content}"
        await discord().send_message(
            channel_id=settings.im.discord.channel_id,
            content=message,
            message_type=MessageType.MailContent,
        )