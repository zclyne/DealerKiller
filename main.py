import asyncio
import logging

from config import settings
from event.dispatcher import default_event_dispatcher
from im.discord.client import discord
from im.discord.events.generated_response import GeneratedResponseEvent
from im.discord.events.new_mail import NewMailEvent
from im.discord.message_type import MessageType
from mail.events.send_email import SendMailEvent
from mail.gmail.gmail import Gmail
from mail.gmail.gmail import get_client as get_gmail_client

logging.basicConfig(level=logging.INFO)


async def main():
    # gmail_client = GmailClient("credentials.json", "token.json")
    # gmail_client.initialize()
    # labels = gmail_client.list_labels()
    # print(labels)
    # messages = gmail_client.list_emails()
    # print(messages)
    # id = "191190f4b943e623"
    # email = gmail_client.get_email(id)
    # print(email.get_content())

    async def send():
        await asyncio.sleep(3)
        # await client.send_message(
        #     "hello from async", message_type=MessageType.MailContent
        # )
        # await client.create_text_channel("test-channel")
        event = SendMailEvent(
            receiver="zyfayanami@gmail.com",
            subject="hello world",
            content="hello world from dealerkiller",
        )
        print("adding send mail event")
        await default_event_dispatcher.put_event(event)
        await asyncio.sleep(30)

    # async def shutdown():
    #     await asyncio.sleep(50)
    #     await default_event_dispatcher.stop()
    #     await get_client().close()

    # task1 = asyncio.create_task(get_client().start(token=settings.im.discord.token))
    task2 = asyncio.create_task(default_event_dispatcher.start())
    # task3 = asyncio.create_task(shutdown())
    task4 = asyncio.create_task(send())
    # await task1
    await task2
    # await task3
    await task4
    # gmail = Gmail.from_dynaconf_settings(settings)
    # emails = gmail.get_unread_inbox(attachments="ignore", max_results=5)
    # print(len(emails))
    # for email in emails:
    #     print(email.date)

    # print(gmail.get_message_by_id("19119627f2ac07ce"))
    # print(get_gmail_client().profile)


if __name__ == "__main__":
    asyncio.run(main())
