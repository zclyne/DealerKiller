import asyncio
import logging
from typing import Awaitable, Callable

from event.event import Event
from event.handler import EventHandler

logger = logging.getLogger(__name__)

_event_handler_registry: dict[str, EventHandler] = {}


def handler(event_type: str):
    """decorator to register a given function as an event handler

    Args:
        event_type (str): type of the event
    """

    def register_handler_inner(cls):
        _event_handler_registry[event_type] = cls()
        return cls

    return register_handler_inner


class EventDispatcher:
    def __init__(self):
        self._queue: asyncio.Queue[Event] = asyncio.Queue()
        self._running = False
        self._lock = asyncio.Lock()
        self._shutdown_event = asyncio.Event()

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
                if event.type in _event_handler_registry:
                    logger.info(f"received new event {event}, executing")
                    handler = _event_handler_registry[event.type]
                    # TODO: deal with handler exception
                    asyncio.create_task(handler.handle(event))
                else:
                    logger.error(f"event {event} has unknown type, skipped")
            except asyncio.TimeoutError:
                if self._shutdown_event.is_set():
                    logger.info("gracefully shutting down")
                    break
            except asyncio.CancelledError:
                logger.info("task is already cancelled")
                break
            except Exception as e:
                print(f"Error processing event {event}, err: {e}")
            finally:
                self._queue.task_done()

        logger.info("draining unfinished events")
        while not self._queue.empty():
            event = self._queue.get_nowait()
            if event.type in _event_handler_registry:
                logger.info(f"received new event {event}, executing")
                handler = _event_handler_registry[event.type]
                await handler(event)
            self._queue.task_done()

        self._shutdown_event.set()

    async def stop(self):
        await self._set_running(False)
        self._shutdown_event.set()
        # wait until the queue is drained
        while not self._queue.empty():
            await asyncio.sleep(0.1)


_default_event_dispatcher = EventDispatcher()


async def start():
    await _default_event_dispatcher.start()


async def stop():
    await _default_event_dispatcher.stop()


async def put_event(event: Event):
    await _default_event_dispatcher.put_event(event)
