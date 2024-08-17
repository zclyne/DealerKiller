import logging

from sqlalchemy.exc import NoResultFound

import database.database as db
from event.dispatcher import put_event
from event.error import WrongEventTypeError
from event.event import Event
from event.handler import EventHandler
from im.discord.event import GeneratedResponseEvent

from .openai import openai
from .prompt import new_mail_prompt, regenerate_response_prompt

logger = logging.getLogger(__name__)

EMAIL_GENERATE_RESPONSE_EVENT = "email_generate_response"
EMAIL_REGENERATE_RESPONSE_EVENT = "email_regenerate_response"


class EmailGenerateResponseEvent(Event):
    def __init__(self, dealer_email: str, subject: str, content: str) -> None:
        self.type: str = EMAIL_GENERATE_RESPONSE_EVENT
        self.dealer_email = dealer_email
        self.subject: str = subject
        self.content: str = content

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, dealer_email={self.dealer_email!r}, subject={self.subject!r}, content={self.content!r})"


class EmailGenerateResponseEventHandler(EventHandler):
    async def handle(self, event: Event):
        if not isinstance(event, EmailGenerateResponseEvent):
            raise WrongEventTypeError(
                f"event {event} is not instance of {EmailGenerateResponseEvent.__name__}"
            )
        logger.info(f"handling email generate response event {event}")

        try:
            # retrieve conversation
            logger.info(f"retrieving conversation for dealer {event.dealer_email}")
            conversation = db.get_conversation_by_email_address(event.dealer_email)
            logger.info(
                f"successfully found conversation for dealer {event.dealer_email}"
            )
        except NoResultFound as e:
            logger.error(
                f"no result found for conversation with email_address={event.dealer_email}, skipping event"
            )
        else:
            prompt = new_mail_prompt(event.subject, event.content)
            response = openai().generate_response(prompt, conversation)
            logger.info(f"putting discord generate_response event")
            discord_generate_response_event = GeneratedResponseEvent(
                event.dealer_email, response
            )
            put_event(discord_generate_response_event)


class EmailRegenerateResponseEvent(Event):
    def __init__(self, dealer_email: str, prompt: str) -> None:
        self.type: str = EMAIL_REGENERATE_RESPONSE_EVENT
        self.dealer_email = dealer_email
        self.prompt: str = prompt

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r}, dealer_email={self.dealer_email!r}, prompt={self.prompt!r})"


class EmailRegenerateResponseEventHandler(EventHandler):
    async def handle(self, event: Event):
        if not isinstance(event, EmailRegenerateResponseEvent):
            raise WrongEventTypeError(
                f"event {event} is not instance of {EmailRegenerateResponseEvent.__name__}"
            )
        logger.info(f"handling email generate response event {event}")

        try:
            # retrieve conversation
            logger.info(f"retrieving conversation for dealer {event.dealer_email}")
            conversation = db.get_conversation_by_email_address(event.dealer_email)
            logger.info(
                f"successfully found conversation for dealer {event.dealer_email}"
            )
        except NoResultFound as e:
            logger.error(
                f"no result found for conversation with email_address={event.dealer_email}, skipping event"
            )
        else:
            prompt = regenerate_response_prompt(event.prompt)
            response = openai().generate_response(prompt, conversation)
            logger.info(f"putting discord generate_response event")
            discord_generate_response_event = GeneratedResponseEvent(
                event.dealer_email, response
            )
            put_event(discord_generate_response_event)
