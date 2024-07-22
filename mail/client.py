from abc import ABC, abstractmethod


class Client(ABC):
    @abstractmethod
    def initialize(self) -> None:
        pass

    @abstractmethod
    def list_labels(self) -> list[str]:
        pass

    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> bool:
        pass

    @abstractmethod
    def list_emails(
        self,
        labels: list[str],
        page_token: str,
        max_results: int,
        include_spam_trash: bool,
    ) -> list[any]:
        pass
