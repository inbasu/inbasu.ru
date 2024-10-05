from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///sqlite.db")
session_maker = async_sessionmaker(engine, autoflush=False)


async def session():
    async with session_maker() as connection:
        yield connection


class Base(DeclarativeBase):  # type: ignore
    pass
