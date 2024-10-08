from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.connection import session_maker
from database.repository import Dictionary
from database.schemas import Word
from .fixtures import hello_word  # noqa


@pytest_asyncio.fixture(loop_scope="session")
async def session() -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as connection:
        yield connection


@pytest.mark.asyncio(loop_scope="session")
async def test_get_item(session: AsyncSession) -> None:
    word = await Dictionary.get_word(session=session, language="fr", value="bonjour")
    assert word is not None
    assert word.__class__ == Word
    assert word.language.name == "fr"
    assert word.translation[0].value == "hello"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_translation(session: AsyncSession, hello_word: Word) -> None:
    bonjour = await Dictionary.get_translation(
        session=session, to="fr", language=hello_word.language.name, value=hello_word.value
    )
    assert bonjour is not None
    assert hello_word.translation[0].value == bonjour.value
    assert hello_word.translation[0].language.name == bonjour.language.name


@pytest.mark.asyncio(loop_scope="session")
async def test_add_word(session: AsyncSession) -> None:
    await Dictionary.add_word(session=session, language="ru", value="привет")
    created = await session.scalar(select(Word).where(Word.value == "привет").options(joinedload(Word.language)))
    assert created is not None
    assert created.__class__ == Word
    assert created.language.name == "ru"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_eng_words(session: AsyncSession) -> None:
    words = await Dictionary.get_all_words(session, "en")
    assert len(words) == 2
    assert words[0].value == "hello"
