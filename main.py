from mail.gmail_client import GmailClient
from im.discord.client import DiscordClient


def main():
    # gmail_client = GmailClient("credentials.json", "token.json")
    # gmail_client.initialize()
    # labels = gmail_client.list_labels()
    # print(labels)
    # messages = gmail_client.list_emails()
    # print(messages)
    # id = "190cd5905771eed9"
    # email = gmail_client.get_email(id)
    # print(email.get_content())
    print("hello")
    client = DiscordClient()
    client.run(token="token")


if __name__ == "__main__":
    main()
