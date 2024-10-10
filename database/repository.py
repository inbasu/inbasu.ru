from abc import ABC, abstractmethod, abstractproperty
from typing import Any, Optional, Sequence, Tuple, Union

from certifi.core import where
from cfgv import NotIn
from dns.e164 import query
from pre_commit.all_languages import languages
from pygments.lexer import words
from sqlalchemy import ScalarResult, Select, and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased, joinedload
from sqlalchemy.sql.selectable import TypedReturnsRows
from watchfiles import awatch

from database.connection import Base
from database.schemas import Language, Word


class Repository(ABC):
    session: AsyncSession
    schema: type[Base]

    async def add(self, entity: object) -> object:
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def update(self, entity: object, **kwargs: str) -> object:
        for attr, value in kwargs.items():
            if hasattr(entity, attr):
                setattr(entity, attr, value)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def get(self, **kwargs) -> Sequence[Base]:  # type: ignore
        results = await self.session.scalars(self._sql(**kwargs))
        return results.unique().all()  # type: ignore

    @abstractmethod
    def _sql(self, **kwargs: str) -> Select[tuple[Base]]:
        return NotImplemented


class Words(Repository):
    schema: type[Base] = Word

    def __init__(self, session: AsyncSession) -> None:
        self.session: AsyncSession = session

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

    async def link(self, *args) -> None:
        words = [arg for arg in args if isinstance(arg, Word)]
        for word in words:
            word.translation.update([w for w in words if w != word])
        await self.session.commit()

    def _sql(self, language: Optional[Language] = None, value: Optional[str] = None, **kwargs) -> Select[tuple[Word]]:  # type: ignore
        lang = f'Language.name ==  "{language.name}"' if language is not None else ""
        val = f'Word.value == "{value}"' if value is not None else ""
        where_condition: str = f".where(and_({','.join([arg for arg in (lang, val) if arg])}))"
        return eval(
            f"select(Word).join(Language){where_condition if where_condition else ''}.options(joinedload(Word.language), joinedload(Word.translation))"
        )
