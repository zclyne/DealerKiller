import asyncio
import logging

from config import settings
from im.discord.client import DiscordClient
from im.discord.message_type import MessageType
from mail.gmail_client import GmailClient

logging.basicConfig(level=logging.INFO)


async def main():
    # gmail_client = GmailClient("credentials.json", "token.json")
    # gmail_client.initialize()
    # labels = gmail_client.list_labels()
    # print(labels)
    # messages = gmail_client.list_emails()
    # print(messages)
    # id = "190cd5905771eed9"
    # email = gmail_client.get_email(id)
    # print(email.get_content())

    discord_settings = settings.im.discord
    client = DiscordClient(
        guild_id=discord_settings.guild_id, channel_id=discord_settings.channel_id
    )

    async def send():
        await asyncio.sleep(20)
        await client.send_message(
            "hello from async", message_type=MessageType.MailContent
        )

    task1 = asyncio.create_task(send())
    task2 = asyncio.create_task(client.start(token=discord_settings.token))
    await task1
    await task2


if __name__ == "__main__":
    asyncio.run(main())
