import discord
from im.discord.ui.prompt_modal import PromptModal


# MailResponseView represents the view sent to the user
# together with a response to an email from a dealer
class MailResponseView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label="Improve Response", style=discord.ButtonStyle.green)
    async def improve_response(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # this button pops up a modal for user to enter the prompt about how to improve the resopnse
        await interaction.response.send_modal(PromptModal())
        self.value = True
        self.stop()

    @discord.ui.button(label="Send Email", style=discord.ButtonStyle.primary)
    async def send(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        # this button sends the mail to the sender
        print("send button clicked")
        # TODO: send mail
        interaction.response.send_message("successfully sent email")
        # TODO: error handling
        self.stop()