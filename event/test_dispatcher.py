import asyncio
import time
from typing import Type

import pytest

from event.error import WrongEventTypeError

from .dispatcher import EventDispatcher, _event_handler_registry, handler
from .event import Event
from .handler import EventHandler


class _TestEvent1(Event):
    def __init__(self):
        self.type = "test_event_1"


class _TestEvent1Handler(EventHandler):
    async def handle(self, event: Event):
        if event.type != "test_event_1" or not isinstance(event, _TestEvent1):
            raise WrongEventTypeError(
                f"event {event} is not instance of {_TestEvent1.__name__}"
            )
        print("test event 1 handler called")


class _TestEvent2(Event):
    def __init__(self):
        self.type = "test_event_2"


class _TestEvent2Handler(EventHandler):
    async def handle(self, event: Event):
        if event.type != "test_event_2" or not isinstance(event, _TestEvent2):
            raise WrongEventTypeError(
                f"event {event} is not instance of {_TestEvent2.__name__}"
            )


class _UnknownTestEvent(Event):
    def __init__(self):
        self.type = "unknown"


@pytest.mark.parametrize(
    "handlers,expected_len",
    [
        ([("test_event_1", _TestEvent1Handler)], 1),
        (
            [
                ("test_event_1", _TestEvent1Handler),
                ("test_event_2", _TestEvent2Handler),
            ],
            2,
        ),
        (
            [
                ("test_event_1", _TestEvent1Handler),
                ("test_event_2", _TestEvent2Handler),
                ("test_event_1", _TestEvent1Handler),  # duplicate registration
            ],
            2,
        ),
    ],
)
def test_handler_decorator(
    handlers: list[tuple[str, Type[EventHandler]]], expected_len: int
):
    # register handlers
    for h in handlers:
        handler(h[0])(h[1])

    assert len(_event_handler_registry) == expected_len
    for h in handlers:
        assert h[0] in _event_handler_registry


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "handlers,error_log",
    [
        ([(_TestEvent1(), _TestEvent1Handler())], None),
        (
            [
                (_TestEvent1(), _TestEvent1Handler()),
                (_TestEvent2(), _TestEvent2Handler()),
            ],
            None,
        ),
    ],
)
async def test_dispatch(
    handlers: list[(Event, EventHandler)], error_log: str | None, caplog, mocker
):
    dispatcher = EventDispatcher()
    # initialization step, register handlers
    for item in handlers:
        event_type = item[0].type
        _event_handler_registry[event_type] = item[1]

    spies = []
    for item in handlers:
        event = item[0]
        handler = item[1]
        await dispatcher.put_event(event)
        # spy the handle function of each handler
        spies.append(mocker.spy(handler, "handle"))

    # start the dispatcher and give it some time to dispatch events to each handler
    asyncio.create_task(dispatcher.start())
    await asyncio.sleep(3)
    await dispatcher.stop()

    # assert each handler is called with the event
    for i in range(len(handlers)):
        event = handlers[i][0]
        spy = spies[i]
        assert spy.call_count == 1
        spy.assert_called_once_with(event)

    # check error log if exists
    if error_log:
        assert error_log in caplog
