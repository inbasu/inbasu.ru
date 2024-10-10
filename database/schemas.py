from typing import Any, Set

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Unpack

from .connection import Base
from sqlalchemy import event


class Translations(Base):
    __tablename__ = "translations"
    id: Mapped[int] = mapped_column(primary_key=True)
    left_id: Mapped[int] = mapped_column(ForeignKey("words.id"))
    right_id: Mapped[str] = mapped_column(ForeignKey("words.id"))


class Language(Base):
    __tablename__ = "languages"

    def __init__(self, **kwargs: str) -> None:
        self.sql: str = ", ".join([f'{self.__class__.__name__}.{arg} == "{value}"' for arg, value in kwargs.items()])
        super().__init__(**kwargs)

    name: Mapped[str] = mapped_column(String(3), primary_key=True)

    @property
    def __sql__(self) -> str:
        return self.sql


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(24))
    lang: Mapped[str] = mapped_column(ForeignKey("languages.name"), nullable=False)
    translation: Mapped[Set["Word"]] = relationship(
        "Word",
        secondary=Translations.__table__,
        primaryjoin=id == Translations.left_id,
        secondaryjoin="Word.id == Translations.right_id",
        lazy="joined",
        back_populates="translation",
    )

    language: Mapped[Language] = relationship(
        Language,
        primaryjoin=lang == Language.name,
        uselist=False,
        lazy="joined",
    )
