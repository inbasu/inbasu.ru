import asyncio

import pytest
import pytest_asyncio
from sqlalchemy import select, text
from sqlalchemy.orm import joinedload

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
        hello: Word = await conn.scalar(select(Word).options(joinedload(Word.translation)))
    return hello


@pytest.mark.asyncio
async def test_database_connection() -> None:
    async with session() as conn:
        assert await conn.scalar(text("SELECT 1 + 1")) == 2


@pytest.mark.asyncio
async def test_word_attrs(hello_word: Word) -> None:
    assert hasattr(hello_word, "value")
    assert hasattr(hello_word, "lang")
    assert hasattr(hello_word, "translation")


@pytest.mark.asyncio
async def test_word_translations(hello_word: Word) -> None:
    assert hello_word.translation[0].value == "bonjour"
    assert hello_word.translation[0].translation[0] == hello_word
