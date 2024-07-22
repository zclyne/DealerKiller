from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from mail.client import Client
import os.path
import logging
import base64
import email
from email.message import EmailMessage


class GmailClient(Client):
    app_credential_file_path: str
    user_token_file_path: str
    creds: Credentials
    service: Resource

    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]

    def __init__(
        self,
        app_credential_file_path: str,
        user_token_file_path: str,
    ) -> None:
        self.app_credential_file_path = app_credential_file_path
        self.user_token_file_path = user_token_file_path
        self.creds = None
        self.service = None

    def initialize(self) -> None:
        self._load_or_refresh_credentials()
        self._build_service()

    def _load_or_refresh_credentials(self) -> None:
        if os.path.exists(self.user_token_file_path):
            self.creds = Credentials.from_authorized_user_file(
                self.user_token_file_path, self.SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                self._run_auth_flow()

        self._save_credentials()

    def _run_auth_flow(self) -> None:
        flow = InstalledAppFlow.from_client_secrets_file(
            self.app_credential_file_path, self.SCOPES
        )
        self.creds = flow.run_local_server(port=0)

    def _save_credentials(self) -> None:
        try:
            with open(self.user_token_file_path, "w") as token:
                token.write(self.creds.to_json())
        except IOError as e:
            self.logger.error(f"Failed to save credentials: {e}")

    def _build_service(self) -> None:
        self.service = build("gmail", "v1", credentials=self.creds)

    def list_labels(self) -> list[dict]:
        results = self.service.users().labels().list(userId="me").execute()

        labels = results.get("labels", [])
        if not labels:
            print("No labels found")
            return []
        return labels

    def send_email(self, to: str, subject: str, body: str) -> bool:
        print("not implemented")

    def list_emails(
        self,
        labels: list[str] = ["INBOX"],
        page_token: str = "",
        max_results: int = 100,
        include_spam_trash: bool = False,
    ) -> list[dict]:
        results = (
            self.service.users()
            .messages()
            .list(
                userId="me",
                labelIds=labels,
                maxResults=max_results,
                includeSpamTrash=include_spam_trash,
                pageToken=page_token,
            )
            .execute()
        )
        messages = results.get("messages", [])
        if not messages:
            print("No messages found")
            return []
        return messages

    def get_email(self, email_id: str) -> EmailMessage:
        message = (
            self.service.users()
            .messages()
            .get(userId="me", id=email_id, format="raw")
            .execute()
        )
        msg_str = base64.urlsafe_b64decode(message["raw"].encode("ascii"))
        mime_msg = email.message_from_bytes(msg_str, policy=email.policy.default)
        return mime_msg
