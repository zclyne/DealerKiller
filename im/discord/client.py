import logging

import discord
from discord import app_commands

from config import settings
from im.discord.message_type import MessageType
from im.discord.ui.mail_response_view import MailResponseView
from im.discord.ui.new_mail_view import NewMailView

logger = logging.getLogger(__name__)


class DiscordClient(discord.Client):
    def __init__(
        self,
        guild_id: int,
        *,
        intents: discord.Intents = discord.Intents.all(),
    ):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because
        # it allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        # TODO: no need to pass guild_id, can get from self.guilds
        self.guild_id = guild_id
        self.tree = app_commands.CommandTree(self)

        # register commands here
        self.tree.add_command(add)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        # FIXME: delete in production
        self.tree.copy_global_to(guild=discord.Object(id=self.guild_id))
        await self.tree.sync(guild=discord.Object(id=self.guild_id))
        # pass

    async def on_ready(self):
        logger.info(f"We have logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content.startswith("hello"):
            await message.channel.send("Hello!")
        if message.content.startswith("prompt"):
            await message.channel.send("prompt test", view=MailResponseView())

    async def send_message(
        self, channel_id: int, content: str, message_type: MessageType
    ):
        channel = self.get_channel(channel_id)
        view = None
        match message_type:
            case MessageType.MailContent:
                view = NewMailView()
            case MessageType.MailResponse:
                view = MailResponseView()
            case _:
                raise ValueError("unknown message type")
        await channel.send(content, view=view)
        logger.info("successfully sent message")

    async def create_text_channel(self, channel_name: str) -> int:
        guild = self.get_guild(self.guild_id)
        if not guild:
            raise RuntimeError(f"guild with id {self.guild_id} not found")
        try:
            channel = await guild.create_text_channel(channel_name)
        except Exception as e:
            logger.error(
                f"failed to create text channel in guild {self.guild_id}, err is {e}"
            )
            raise e
        return channel.id


# @app_commands.command()
# async def register(interaction: discord.Interaction):
#     """Register the user who executed this command to DealerKiller

#     Registration adds a record into the database with the user id
#     who executed this command, together the guild from which the
#     command was run. In the future, all the emails related to this
#     user will be sent into this guild.

#     Args:
#         interaction (discord.Interaction): a discord Interaction object
#         representing the command
#     """
#     pass
#     # TODO: store the guild id and user id into database


@app_commands.command()
@app_commands.describe(
    first_value="The first value you want to add something to",
    second_value="The value you want to add to the first value",
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(
        f"{first_value} + {second_value} = {first_value + second_value}"
    )


_default_discord_client = DiscordClient(guild_id=settings.im.discord.guild_id)


def get_client() -> DiscordClient:
    return _default_discord_client
