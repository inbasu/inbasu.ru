import asyncio

import pytest
from sqlalchemy import select

from database.connection import session_maker
from database.repository import Dictionary
from database.schemas import Word

from .fixtures import create_table, drop_table


def setup_module() -> None:
    asyncio.run(create_table())


def teardown_module() -> None:
    asyncio.run(drop_table())


@pytest.fixture
def dictionary() -> Dictionary:
    return Dictionary(session_maker)


@pytest.mark.asyncio
async def test_add_word(dictionary) -> None:
    await dictionary.add(Word(value="hello", lang="eng"))
    async with session_maker() as s:
        hello: Word = await s.scalar(select(Word).where(Word.value == "hello"))
    assert hello.value == "hello"


@pytest.mark.asyncio
async def test_get_word_with_params() -> None:
    assert False


# @pytest.mark.asyncio
# async def test_create_with_translation() -> None:
#     assert False
