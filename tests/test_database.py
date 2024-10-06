import asyncio

import fixtup
import pytest
import pytest_asyncio
from sqlalchemy import select, text

from database.connection import session_maker
from database.schemas import Language, Word

from .fixtures import create_table, create_word_hello, drop_table, hello_word  # noqa


def setup_module() -> None:
    with fixtup.up("mysql"):
        asyncio.run(create_table())
        asyncio.run(create_word_hello())


def teardown_module() -> None:
    asyncio.run(drop_table())


@pytest_asyncio.fixture
async def eng() -> Language:
    async with session_maker() as conn:
        eng: Language = await conn.scalar(select(Language).where(Language.name == "en"))
    return eng


@pytest.mark.asyncio
async def test_database_connection() -> None:
    async with session_maker() as conn:
        assert await conn.scalar(text("SELECT 1 + 1")) == 2


@pytest.mark.asyncio
async def test_word_attrs(hello_word: Word) -> None:
    assert hasattr(hello_word, "value")
    assert hasattr(hello_word, "language")
    assert hasattr(hello_word, "translation")


@pytest.mark.asyncio
async def test_word_translations(hello_word: Word) -> None:
    assert hello_word.translation[0].value == "bonjour"
    assert hello_word.translation[0].translation[0] == hello_word
    assert hello_word.language.name == "en"


@pytest.mark.asyncio
async def test_lang_attrs(eng: Language) -> None:
    assert hasattr(eng, "name")


@pytest.mark.asyncio
async def test_get_eng_words(eng: Language) -> None:
    async with session_maker() as s:
        query = await s.scalars(select(Word).where(Word.language == eng))
    words = query.unique().all()
    assert len(words) == 1
    assert words[0].value == "hello"


@pytest.mark.asyncio
async def test_language_property(eng: Language, hello_word: Word) -> None:
    assert hello_word.language.id == eng.id
    assert hello_word.language.name == eng.name
