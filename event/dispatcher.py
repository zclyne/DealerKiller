import asyncio
import logging
from typing import Awaitable, Callable

from event.event import Event
from event.handler import EventHandler

logger = logging.getLogger(__name__)


class EventDispatcher:
    def __init__(self):
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._handlers: dict[str, EventHandler] = {}
        self._running = False
        self._lock = asyncio.Lock()
        self._shutdown_event = asyncio.Event()

    async def register(self, event_type: str, handler: EventHandler) -> None:
        async with self._lock:
            if event_type in self._handlers:
                logger.warning(
                    f"duplicate handler registered for event_type {event_type}, old value will be overriden"
                )
            self._handlers[event_type] = handler

    async def put_event(self, event: Event):
        await self._queue.put(event)

    async def _is_running(self):
        async with self._lock:
            return self._running

    async def _set_running(self, value: bool):
        async with self._lock:
            self._running = value

    async def start(self):
        logger.info(f"starting event dispatcher")
        await self._set_running(True)
        while await self._is_running():
            try:
                event = await asyncio.wait_for(self._queue.get(), timeout=1.0)
                if event.type in self._handlers:
                    logger.info(f"received new event {event}, executing")
                    handler = self._handlers[event.type]
                    # TODO: deal with handler exception
                    asyncio.create_task(handler.handle(event))
                else:
                    logger.error(f"event {event} has unknown type, skipped")
                self._queue.task_done()
            except asyncio.TimeoutError:
                if self._shutdown_event.is_set():
                    logger.info("gracefully shutting down")
                    break
            except Exception as e:
                print(f"Error processing event {event}, err: {e}")

        logger.info("draining unfinished events")
        while not self._queue.empty():
            event = self._queue.get_nowait()
            if event.type in self._handlers:
                logger.info(f"received new event {event}, executing")
                handler = self._handlers[event.type]
                await handler(event)
            self._queue.task_done()

        self._shutdown_event.set()

    async def stop(self):
        await self._set_running(False)
        self._shutdown_event.set()


default_event_dispatcher = EventDispatcher()
