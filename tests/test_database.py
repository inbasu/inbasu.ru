import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import select, text

from database.connection import session
from database.schemas import Word

from .fixtures import create_table, create_word_hello, drop_table


def setup_module() -> None:
    asyncio.run(create_table())
    asyncio.run(create_word_hello())


def teardown_module() -> None:
    asyncio.run(drop_table())


@pytest_asyncio.fixture
async def hello_word() -> Word:
    async with session() as conn:
        hello = await conn.scalar(select(Word))
    return hello


@pytest.mark.asyncio
async def test_database_connection() -> None:
    async with session() as conn:
        assert await conn.scalar(text("SELECT 1 + 1")) == 2


@pytest.mark.asyncio
async def test_word_attrs(hello_word) -> None:
    assert hello_word.value == "hello"
