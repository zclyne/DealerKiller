import discord
from im.discord.ui.prompt_modal import PromptModal


# NewMailView represents the view sent to the user
# together with a new mail content
class NewMailView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Generate Response", style=discord.ButtonStyle.green)
    async def improve_response(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # this button calls LLM to generate a response based on the mail content
        # TODO: generate response
        await interaction.response.send_message("successfully sent generated response")
        # TODO: send response
        self.stop()
