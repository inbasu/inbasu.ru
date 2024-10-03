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
        w1 = Word(value="hello", lang="en")
        w2 = Word(value="bonjour", lang="fr")
        w1.translation = [w2]
        w2.translation = [w1]
        s.add_all([w1, w2])
        await s.commit()
