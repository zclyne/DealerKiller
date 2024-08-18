import pytest

from .dispatcher import _event_handler_registry


@pytest.fixture(autouse=True)
def clean_up_registry():
    yield
    _event_handler_registry.clear()
