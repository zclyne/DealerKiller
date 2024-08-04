from dataclasses import dataclass


@dataclass
class Event:
    type: str

    def __repr__(self):
        return f"{self.__class__.__name__}(type={self.type!r})"
