import pytest_asyncio
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from database.connection import Base, engine, session_maker
from database.schemas import Language, Word


async def create_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_word_hello() -> None:
    await create_lang()
    async with session_maker() as s:
        en: Language = await s.scalar(select(Language).where(Language.name == "en"))
        fr: Language = await s.scalar(select(Language).where(Language.name == "fr"))
        w1: Word = Word(value="hello", language=en)
        w2: Word = Word(value="bonjour", language=fr)
        w1.translation = [w2]
        w2.translation = [w1]
        s.add_all([w1, w2])
        await s.commit()


async def create_lang() -> None:
    async with session_maker() as s:
        s.add_all([Language(name="en"), Language(name="fr"), Language(name="ru")])
        await s.commit()


@pytest_asyncio.fixture
async def hello_word() -> Word:
    async with session_maker() as conn:
        hello: Word = await conn.scalar(select(Word).options(joinedload(Word.translation), joinedload(Word.language)))
    return hello
