from typing import Optional, Union

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from database.schemas import Language, Word


class Dictionary:

    @classmethod
    async def get_word(cls, session: AsyncSession, value: str, language: str) -> Optional[Word]:
        result: Union[Word, None] = await session.scalar(
            select(Word)
            .join(Language)
            .where(and_(Word.value == value, Language.name == language))
            .options(joinedload(Word.language), joinedload(Word.translation))
        )
        return result

    @classmethod
    async def get_translation(cls, session: AsyncSession, language: str, value: str) -> Optional[Word]:
        word = aliased(Word)
        result: Union[Word, None] = await session.scalar(
            select(Word)
            .join(Language)
            .join(Word.translation.of_type(word))
            .where(and_(Word.translation.any(word.value == value), Language.name == language))
            .options(joinedload(Word.language), joinedload(Word.translation))
        )
        return result

    @classmethod
    async def add_word(cls, session: AsyncSession, value: str, language: str):
        lang = await session.scalar(select(Language).where(Language.name == language))
        word = Word(value=value, language=lang)
        session.add(word)
        await session.commit()
        return word


#     @classmethod
#     async def set_translation(cls):
#         pass
