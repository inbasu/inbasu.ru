import pytest
import pytest_asyncio
from sqlalchemy import select, text

from database.connection import session_maker
from database.schemas import Language, Word

from .fixtures import (  # noqa
    create_table,
    create_word_hello,
    drop_table,
    eng,
    hello_word,
)


@pytest_asyncio.fixture(autouse=True, scope="session")
async def setup_module() -> None:
    await drop_table()
    await create_table()
    await create_word_hello()


@pytest.mark.asyncio(loop_scope="session")
async def test_database_connection() -> None:
    async with session_maker() as conn:
        assert await conn.scalar(text("SELECT 1 + 1")) == 2


@pytest.mark.asyncio(loop_scope="session")
async def test_word_attrs(hello_word: Word) -> None:
    assert hasattr(hello_word, "value")
    assert hasattr(hello_word, "language")
    assert hasattr(hello_word, "translation")


@pytest.mark.asyncio(loop_scope="session")
async def test_word_translations(hello_word: Word) -> None:
    assert list(hello_word.translation)[0].value == "bonjour"
    assert hello_word in list(hello_word.translation)[0].translation
    assert hello_word.language.name == "en"


@pytest.mark.asyncio(loop_scope="session")
async def test_lang_attrs(eng: Language) -> None:
    assert hasattr(eng, "name")


@pytest.mark.asyncio(loop_scope="session")
async def test_get_eng_words(eng: Language) -> None:
    async with session_maker() as s:
        query = await s.scalars(select(Word).where(Word.language == eng))
    words = query.unique().all()
    assert len(words) == 2
    assert words[0].value == "hello"


@pytest.mark.asyncio(loop_scope="session")
async def test_language_property(eng: Language, hello_word: Word) -> None:
    assert hello_word.language.name == eng.name
