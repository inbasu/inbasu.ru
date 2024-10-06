from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("mysql+aiomysql://user:password@localhost/dbname?charset=utf8mb4")
session_maker = async_sessionmaker(engine, autoflush=False)


async def session() -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as connection:
        yield connection


class Base(DeclarativeBase):  # type: ignore
    pass
