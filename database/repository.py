from sqlalchemy.ext.asyncio import async_sessionmaker

from .schemas import Word


class Dictionary:

    def __init__(self, session_maker) -> None:
        self.session_maker: async_sessionmaker = session_maker

    async def add(self, word: Word) -> Word:
        async with self.session_maker() as s:
            s.add(word)
            await s.commit()
        return word
