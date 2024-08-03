import asyncio
import logging

from config import settings
from event.dispatcher import default_event_dispatcher
from event.error import WrongEventTypeError
from event.event import Event
from event.handler import EventHandler
from mail.gmail.gmail import get_client

SEND_MAIL_EVENT = "send_mail"

logger = logging.getLogger(__name__)


class SendMailEvent(Event):
    def __init__(self, receiver: str, subject: str, content: str) -> None:
        # TODO: support attachment
        self.type: str = SEND_MAIL_EVENT
        self.receiver: str = receiver
        self.subject: str = subject
        self.content: str = content

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, receiver={self.receiver!r}, subject={self.subject!r}, content={self.content!r})"


class SendMailEventHandler(EventHandler):
    async def handle(self, event: Event):
        if not isinstance(event, SendMailEvent):
            raise WrongEventTypeError(
                f"event {event} is not instance of {SendMailEvent.__name__}"
            )
        logger.info(f"handling send mail event {event}")
        try:
            message = get_client().send_message(
                to=event.receiver,
                subject=event.subject,
                msg_plain=event.content,
            )
        except Exception as e:
            logger.error(f"failed to send mail, err is {e}")
        else:
            logger.info(f"successfully sent mail {message}")
        # TODO: error handling


asyncio.run(default_event_dispatcher.register(SEND_MAIL_EVENT, SendMailEventHandler()))
