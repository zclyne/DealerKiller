from abc import ABC, abstractmethod

from event.event import Event


class EventHandler(ABC):
    @abstractmethod
    async def handle(self, event: Event):
        pass
