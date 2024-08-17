from contextlib import AbstractContextManager
from contextlib import nullcontext as does_not_raise

import pytest
from sqlalchemy import Engine, event
from sqlalchemy.exc import IntegrityError, NoResultFound
from sqlalchemy.orm import Session

from . import database as db
from .conversation import Conversation
from .message import Message


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Enable foreign key constraint of sqlite
    refer to: https://docs.sqlalchemy.org/en/20/dialects/sqlite.html#foreign-key-support
    """
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.mark.parametrize(
    "existing_conversations,new_email,expected",
    [
        ([Conversation(dealer_email="qwer@toyoda.com")], "asdf@honda.com", True),
        ([Conversation(dealer_email="qwer@honda.com")], "asdf@honda.com", True),
        ([], "asdf@honda.com", True),
        (
            [
                Conversation(dealer_email="qwer@toyota.com"),
                Conversation(
                    dealer_email="asdf@honda.com",
                ),
            ],
            "asdf@honda.com",
            False,
        ),
    ],
)
def test_insert_conversation_if_not_exist(
    existing_conversations: list[Conversation],
    new_email: str,
    expected: bool,
    engine: Engine,
):
    initialize_conversations(existing_conversations, engine)

    result = db.insert_conversation_if_not_exist(new_email, engine=engine)
    assert result == expected


@pytest.mark.parametrize(
    "existing_conversations,new_email,expectation",
    [
        (
            [Conversation(dealer_email="qwer@toyota.com")],
            "asdf@honda.com",
            does_not_raise(),
        ),
        (
            [Conversation(dealer_email="qwer@honda.com")],
            "asdf@honda.com",
            does_not_raise(),
        ),
        ([], "asdf@honda.com", does_not_raise()),
        (
            [
                Conversation(dealer_email="qwer@toyota.com"),
                Conversation(dealer_email="asdf@honda.com"),
            ],
            "asdf@honda.com",
            pytest.raises(IntegrityError),
        ),
    ],
)
def test_insert_conversation(
    existing_conversations: list[Conversation],
    new_email: str,
    expectation: AbstractContextManager,
    engine: Engine,
):
    initialize_conversations(existing_conversations, engine)

    with expectation:
        db.insert_conversation(new_email, engine=engine)


@pytest.mark.parametrize(
    "existing_conversations,email_to_find,expectation",
    [
        (
            [Conversation(dealer_email="qwer@honda.com")],
            "qwer@honda.com",
            does_not_raise(),
        ),
        (
            [Conversation(dealer_email="qwer@honda.com")],
            "asdf@honda.com",
            pytest.raises(NoResultFound),
        ),
        ([], "asdf@honda.com", pytest.raises(NoResultFound)),
        (
            [
                Conversation(dealer_email="qwer@toyota.com"),
                Conversation(dealer_email="asdf@honda.com"),
                Conversation(dealer_email="1234@mazda.com"),
            ],
            "asdf@honda.com",
            does_not_raise(),
        ),
        (
            [
                Conversation(dealer_email="qwer@toyota.com"),
                Conversation(dealer_email="qwer@honda.com"),
            ],
            "zxcv@honda.com",
            pytest.raises(NoResultFound),
        ),
    ],
)
def test_get_conversation_by_email_address(
    existing_conversations: list[Conversation],
    email_to_find: str,
    expectation: AbstractContextManager,
    engine: Engine,
):
    initialize_conversations(existing_conversations, engine)

    with expectation:
        db.get_conversation_by_email_address(email_to_find, engine=engine)


@pytest.mark.parametrize(
    "existing_conversations,existing_messages,new_message,expectation",
    [
        (
            [
                Conversation(id=1, dealer_email="asdf@honda.com"),
            ],
            [
                Message(
                    id=1,
                    role="user",
                    content="hello world",
                    status="draft",
                    conversation_id=1,
                ),
            ],
            Message(role="assistant", content="what's up", conversation_id=1),
            does_not_raise(),
        ),
        (
            [
                Conversation(id=1, dealer_email="asdf@honda.com"),
            ],
            [
                Message(
                    id=1,
                    role="user",
                    content="hello world",
                    status="draft",
                    conversation_id=1,
                ),
            ],
            Message(role="assistant", content="what's up", conversation_id=2),
            pytest.raises(IntegrityError),
        ),
        (
            [],
            [],
            Message(role="assistant", content="what's up", conversation_id=2),
            pytest.raises(IntegrityError),
        ),
    ],
)
def test_insert_message(
    existing_conversations: list[Conversation],
    existing_messages: list[Message],
    new_message: Message,
    expectation: AbstractContextManager,
    engine: Engine,
):
    initialize_conversations(existing_conversations, engine)
    initialize_messages(existing_messages, engine)

    with expectation:
        m = db.insert_message(
            new_message.role, new_message.content, new_message.conversation_id, engine
        )
        assert m.status == "draft"


@pytest.mark.parametrize(
    "existing_conversations,existing_messages,message_id_to_get,expected_message,expectation",
    [
        (
            [
                Conversation(id=1, dealer_email="asdf@honda.com"),
            ],
            [
                Message(
                    id=1,
                    role="user",
                    content="hello world",
                    status="draft",
                    conversation_id=1,
                ),
            ],
            1,
            Message(
                id=1,
                role="user",
                content="hello world",
                status="draft",
                conversation_id=1,
            ),
            does_not_raise(),
        ),
        (
            [
                Conversation(id=1, dealer_email="asdf@honda.com"),
            ],
            [
                Message(
                    id=1,
                    role="user",
                    content="hello world",
                    status="draft",
                    conversation_id=1,
                ),
                Message(
                    id=2,
                    role="assistant",
                    content="what's up",
                    status="draft",
                    conversation_id=1,
                ),
            ],
            2,
            Message(
                id=2,
                role="assistant",
                content="what's up",
                status="draft",
                conversation_id=1,
            ),
            does_not_raise(),
        ),
        (
            [
                Conversation(id=1, dealer_email="asdf@honda.com"),
            ],
            [
                Message(
                    id=1,
                    role="user",
                    content="hello world",
                    status="draft",
                    conversation_id=1,
                ),
                Message(
                    id=2,
                    role="assistant",
                    content="what's up",
                    status="draft",
                    conversation_id=1,
                ),
            ],
            3,
            Message(),
            pytest.raises(NoResultFound),
        ),
    ],
)
def test_get_message_by_id(
    existing_conversations: list[Conversation],
    existing_messages: list[Message],
    message_id_to_get: int,
    expected_message: Message,
    expectation: AbstractContextManager,
    engine: Engine,
):
    initialize_conversations(existing_conversations, engine)
    initialize_messages(existing_messages, engine)

    with expectation:
        m = db.get_message_by_id(message_id_to_get, engine)
        assert m.id == expected_message.id
        assert m.role == expected_message.role
        assert m.content == expected_message.content
        assert m.conversation_id == expected_message.conversation_id


# util functions to initialize the db
def initialize_messages(messages: list[Message], engine: Engine):
    with Session(engine) as session:
        session.add_all(messages)
        session.commit()


def initialize_conversations(conversations: list[Conversation], engine: Engine):
    with Session(engine) as session:
        session.add_all(conversations)
        session.commit()
