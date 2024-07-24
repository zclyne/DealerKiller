from typing import Optional
import logging
import discord
from discord import app_commands
from im.discord.ui.mail_response_view import MailResponseView
from im.discord.ui.new_mail_view import NewMailView
from im.discord.message_type import MessageType

MY_GUILD = discord.Object(id=1264372372295647353)
ZK_GUILD = discord.Object(id=1051311876941811763)

logger = logging.getLogger(__name__)

class DiscordClient(discord.Client):
    def __init__(self, channel_id: int, *, intents: discord.Intents = discord.Intents.all()):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.channel_id = channel_id
        self.tree = app_commands.CommandTree(self)

        # register commands here
        self.tree.add_command(add)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)
        self.tree.copy_global_to(guild=ZK_GUILD)
        await self.tree.sync(guild=ZK_GUILD)

    async def on_ready(self):
        logger.info(f"We have logged in as {self.user}")

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return

        if message.content.startswith("hello"):
            await message.channel.send("Hello!")
        if message.content.startswith("prompt"):
            await message.channel.send("prompt test", view=MailResponseView())

    async def send_message(self, content: str, message_type: MessageType):
        channel = await self.fetch_channel(self.channel_id)
        view = None
        match message_type:
            case MessageType.MailContent:
                view=NewMailView()
            case MessageType.MailResponse:
                view=MailResponseView()  
        await channel.send(content, view=view)
        logger.info("successfully sent message")

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
