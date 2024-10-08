from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from database.connection import session_maker
from database.repository import Words
from database.schemas import Language, Word

from .fixtures import hello_word  # noqa


@pytest_asyncio.fixture(loop_scope="session")
async def session() -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as connection:
        yield connection


@pytest.mark.asyncio(loop_scope="session")
async def test_get_item(session: AsyncSession) -> None:
    word = await Words(session).get_word(language="fr", value="bonjour")
    assert word is not None
    assert word.__class__ == Word
    assert word.language.name == "fr"
    assert word.translation[0].value == "hello"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_translation(session: AsyncSession, hello_word: Word) -> None:
    bonjour = await Words(session).get_translation(to="fr", language=hello_word.language.name, value=hello_word.value)
    assert bonjour is not None
    assert hello_word.translation[0].value == bonjour.value
    assert hello_word.translation[0].language.name == bonjour.language.name


@pytest.mark.asyncio(loop_scope="session")
async def test_add_word(session: AsyncSession) -> None:
    to_create = await Words(session).add(
        entity=Word(
            language=await session.scalar(select(Language).where(Language.name == "ru")),
            value="привет",
        )
    )
    created = await session.scalar(select(Word).where(Word.value == "привет").options(joinedload(Word.language)))
    assert created is not None
    assert to_create == created


@pytest.mark.asyncio(loop_scope="session")
async def test_get_eng_words(session: AsyncSession) -> None:
    words = await Words(session).get_all_words(Language(name="en"))
    assert len(words) == 2
    assert words[0].value == "hello"


@pytest.mark.asyncio(loop_scope="session")
async def test_update_word(session: AsyncSession) -> None:
    word = Word(
        language=await session.scalar(select(Language).where(Language.name == "fr")),
        value="vrai",
    )
    session.add(word)
    await session.commit()
    await session.refresh(word)
    updated = await Words(session).update(word, value="faux")
    assert updated.__class__ == Word
    assert updated.value == "faux"
