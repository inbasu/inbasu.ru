from typing import Any, AsyncGenerator, Sequence
from venv import create

import pytest
import pytest_asyncio
from anyio.abc import value
from pre_commit.all_languages import languages
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
    words: Sequence[Word] = await Words(session).get(language=Language(name="fr"), value="bonjour")
    assert words is not None
    assert words[0].__class__ == Word
    assert words[0].language.name == "fr"
    assert list(words[0].translation)[0].value == "hello"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_translation(session: AsyncSession, hello_word: Word) -> None:
    bonjour = await Words(session).get_translation(to="fr", language=hello_word.language.name, value=hello_word.value)
    assert bonjour is not None
    assert list(hello_word.translation)[0].value == bonjour.value
    assert list(hello_word.translation)[0].language.name == bonjour.language.name


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
    words = await Words(session).get(language=Language(name="en"))
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
    updated: Word = await Words(session).update(word, value="faux")  # type: ignorgite
    assert updated.__class__ == Word
    assert updated.value == "faux"


@pytest.mark.asyncio(loop_scope="session")
async def test_link_words(session: AsyncSession) -> None:
    created: Word = Word(value="hi", language=await session.scalar(select(Language).where(Language.name == "en")))
    session.add(created)
    await session.commit()
    await Words(session).link(
        await session.scalar(select(Word).where(Word.value == "hi").options(joinedload(Word.translation))),
        await session.scalar(select(Word).where(Word.value == "bonjour").options(joinedload(Word.translation))),
    )
    created = await session.scalar(select(Word).where(Word.value == "hi").options(joinedload(Word.translation)))
    word = await session.scalar(select(Word).where(Word.value == "bonjour").options(joinedload(Word.translation)))
    assert created in word.translation
    assert word in created.translation
