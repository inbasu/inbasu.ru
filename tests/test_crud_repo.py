import asyncio

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession

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
async def session() -> AsyncSession:
    return session_maker()


@pytest.mark.asyncio
async def test_get_item(session: AsyncSession) -> None:
    word = await Dictionary.get(session=session, language="fr", value="bonjour")
    await session.close()
    assert word.__class__ == Word
    assert word.language.name == "fr" if word is not None else False
    assert word.translation[0].value == "hello" if word is not None else False


@pytest.mark.asyncio
async def test_get_translation(session: AsyncSession, hello_word: Word) -> None:
    bonjour = await Dictionary.get_translation(session, language="fr", value=hello_word.value)
    assert hello_word.translation[0].value == bonjour.value if bonjour is not None else False
    assert hello_word.translation[0].language.name == bonjour.language.name if bonjour is not None else False
