import logging
import time

import schedule

from config import settings

from .gmail.gmail import get_client

gmail_client = get_client()
logger = logging.getLogger(__name__)


def check_new_mails():
    emails = gmail_client.get_unread_inbox(max_results=settings.email.gmail.batch_size)
    for email in emails:
        if not is_dealer(email.sender):
            logger.info(
                f"email sender {email.sender} is not likely to be a dealer, skipped"
            )
            continue
        logger.info(
            f"found new email from dealer {email.sender}, subject={email.subject}"
        )
        # check whether conversation exists and create conversation if necessary
        

        # TODO: save new message to db

        # TODO: send to discord


def is_dealer(email_address: str) -> bool:
    """returns whether a certain email_address is likely to belong to a dealer

    Args:
        email_address (str): email address of a new email

    Returns:
        bool: whether the email_address might belong to a dealer or not
    """
    for brand in settings.dealer.brands:
        if brand.lower() in email_address.lower():
            return True
    return False
