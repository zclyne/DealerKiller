import discord
import traceback


class PromptModal(discord.ui.Modal, title="Improve the Response"):
    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    feedback = discord.ui.TextInput(
        label="How would you like to respond?",
        style=discord.TextStyle.long,
        placeholder="Enter your prompt for the LLM here...",
        required=True,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        # TODO: send prompt to LLM
        await interaction.response.send_message(
            f"Thanks for your feedback, {self.name.value}!", ephemeral=True
        )

    async def on_error(
        self, interaction: discord.Interaction, error: Exception
    ) -> None:
        # TODO: better error handling
        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )

        # Make sure we know what the error actually is
        traceback.print_exception(type(error), error, error.__traceback__)
