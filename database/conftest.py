import pytest
from sqlalchemy import create_engine

from .base import Base


@pytest.fixture
def engine():
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
