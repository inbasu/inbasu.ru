import pytest
import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.connection import Base, engine, session_maker
from database.schemas import Language, Word


@pytest.mark.asyncio
async def create_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@pytest.mark.asyncio
async def drop_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.mark.asyncio(loop_scope="session")
async def create_word_hello() -> None:
    await create_lang()
    async with session_maker() as s:
        en: Language = await s.scalar(select(Language).where(Language.name == "en"))
        fr: Language = await s.scalar(select(Language).where(Language.name == "fr"))
        w1: Word = Word(value="hello", language=en)
        w2: Word = Word(value="bonjour", language=fr)
        w3: Word = Word(value="world", language=en)
        s.add_all([w1, w2, w3])
        w1.translation.add(w2)
        w2.translation.add(w1)
        await s.commit()


@pytest.mark.asyncio
async def create_lang() -> None:
    async with session_maker() as s:
        s.add_all([Language(name="en"), Language(name="fr"), Language(name="ru")])
        await s.commit()


@pytest_asyncio.fixture(scope="session")
async def eng() -> Language:
    async with session_maker() as conn:
        eng: Language = await conn.scalar(select(Language).where(Language.name == "en"))
    return eng


@pytest_asyncio.fixture(scope="session")
async def hello_word() -> Word:
    async with session_maker() as conn:
        hello: Word = await conn.scalar(select(Word).options(joinedload(Word.translation), joinedload(Word.language)))
    return hello
