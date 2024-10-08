from abc import ABC
from typing import Any, Optional, Sequence, Union

from sqlalchemy import ScalarResult, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload

from database.connection import Base
from database.schemas import Language, Word


class Repository(ABC):
    session: AsyncSession
    schema: Base

    async def add(self, entity: object) -> object:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: object, **kwargs: dict[str, Any]) -> object:
        for attr, value in kwargs.items():
            if hasattr(entity, attr):
                setattr(entity, attr, value)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity


class Words(Repository):
    schema: Word

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

    async def get_word(self, value: str, language: str) -> Optional[Word]:
        result: Union[Word, None] = await self.session.scalar(
            select(Word)
            .join(Language)
            .where(and_(Word.value == value, Language.name == language))
            .options(joinedload(Word.language), joinedload(Word.translation))
        )
        return result

    async def get_all_words(self, language: Union[Language, None]) -> Sequence[Word]:
        sequance: ScalarResult = await self.session.scalars(
            select(Word).join(Language).where(Language.name == language.name).order_by(Word.value)
        )
        result: Sequence[Word] = sequance.unique().all()
        return result

    async def get_translation(self, language: str, value: str, to: str) -> Optional[Word]:
        word = aliased(Word)
        lang = aliased(Language)
        result: Union[Word, None] = await self.session.scalar(
            select(Word)
            .join(Language)
            .join(Word.translation.of_type(word))
            .join(word.language.of_type(lang))
            .where(
                and_(
                    Word.translation.any(word.value == value),
                    Word.translation.any(lang.name == language),
                    Language.name == to,
                )
            )
            .options(joinedload(Word.language))
        )
        return result


#     @classmethod
#     async def set_translation(cls):
#         pass
