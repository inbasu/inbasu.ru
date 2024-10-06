from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

try:

    raise NotImplementedError
#    dotenv.load_dotenv()
#    engine = create_async_engine(
#        "mysql+aiomysql://{}:{}@localhost/{}?charset=utf8mb4",
#        pool_pre_ping=True,
#    )
except:
    engine = create_async_engine("sqlite+aiosqlite:///sqlite.db")


session_maker = async_sessionmaker(engine, autoflush=False)


async def session() -> AsyncGenerator[AsyncSession, Any]:
    async with session_maker() as connection:
        yield connection


class Base(DeclarativeBase):  # type: ignore
    pass
