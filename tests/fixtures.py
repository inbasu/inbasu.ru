from database.connection import Base, engine, session
from database.schemas import Word


async def create_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_table() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_word_hello() -> None:
    async with session() as s:
        s.add(Word(value="hello"))
        await s.commit()
