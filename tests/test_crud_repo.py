import asyncio
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.connection import session_maker
from database.repository import Dictionary
from database.schemas import Word

from .fixtures import create_table, create_word_hello, drop_table, hello_word  # noqa


def setup_module() -> None:
    asyncio.run(create_table())
    asyncio.run(create_word_hello())


def teardown_module() -> None:
    asyncio.run(drop_table())


@pytest_asyncio.fixture
<<<<<<< HEAD
async def session() -> AsyncSession:
    """В fastAPI в Depend передается сессия,
    и онa будет передваться в репозиторий внутри view,
    поэтому в тестах try:...finally:..."""
    return session_maker()
=======
async def session() -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as connection:
        yield connection
>>>>>>> 17cbd6aaaaa29d5fe59d79bf775f235d8d1056c6


@pytest.mark.asyncio
async def test_get_item(session: AsyncSession) -> None:
<<<<<<< HEAD
    try:
        word = await Dictionary.get_word(session=session, language="fr", value="bonjour")
        await session.close()
        assert word.__class__ == Word
        assert word.language.name == "fr" if word is not None else False
        assert word.translation[0].value == "hello" if word is not None else False
    finally:
        await session.close()
=======
    word = await Dictionary.get(session=session, language="fr", value="bonjour")
    assert word.__class__ == Word
    assert word.language.name == "fr" if word is not None else False
    assert word.translation[0].value == "hello" if word is not None else False
>>>>>>> 17cbd6aaaaa29d5fe59d79bf775f235d8d1056c6


@pytest.mark.asyncio
async def test_get_translation(session: AsyncSession, hello_word: Word) -> None:
<<<<<<< HEAD
    try:
        bonjour = await Dictionary.get_translation(session, language="fr", value=hello_word.value)
        assert hello_word.translation[0].value == bonjour.value if bonjour is not None else False
        assert hello_word.translation[0].language.name == bonjour.language.name if bonjour is not None else False
    finally:
        await session.close()


@pytest.mark.asyncio
async def test_add_word(session: AsyncSession) -> None:
    try:
        await Dictionary.add_word(session, language="ru", value="привет")
        created = await session.scalar(select(Word).where(Word.value == "привет").options(joinedload(Word.language)))
        assert created.__class__ == Word
        assert created.language.name == "ru"
    finally:
        await session.close()


# @pytest.mark.asyncio
# async def test_set_translation(session: AsyncSession, hello_word: Word) -> None:
#     try:
#         assert False
#     finally:
#         await session.close()
=======
    bonjour = await Dictionary.get_translation(
        session, to="fr", language=hello_word.language.name, value=hello_word.value
    )
    assert hello_word.translation[0].value == bonjour.value if bonjour is not None else False
    assert hello_word.translation[0].language.name == bonjour.language.name if bonjour is not None else False
>>>>>>> 17cbd6aaaaa29d5fe59d79bf775f235d8d1056c6
