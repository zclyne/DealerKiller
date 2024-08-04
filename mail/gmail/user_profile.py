from dataclasses import dataclass


@dataclass
class UserProfile:
    email_address: str
    messages_total: int
    threads_total: int
    history_id: str
