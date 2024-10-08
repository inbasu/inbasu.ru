from typing import Any, List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Unpack

from .connection import Base

translations = Table(
    "translations",
    Base.metadata,
    Column("left_id", ForeignKey("words.id"), primary_key=True),
    Column("right_id", ForeignKey("words.id"), primary_key=True),
)


class Language(Base):
    __tablename__ = "languages"

    def __init__(self, **kwargs: str) -> None:
        self.sql: str = ", ".join([f'{self.__class__.__name__}.{arg} == "{value}"' for arg, value in kwargs.items()])
        super().__init__(**kwargs)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(3), unique=True)

    @property
    def __sql__(self) -> str:
        return self.sql


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(24))
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"), nullable=False)
    translation: Mapped[List["Word"]] = relationship(
        secondary=translations,
        primaryjoin=id == translations.c.left_id,
        secondaryjoin=id == translations.c.right_id,
        lazy="joined",
    )

    language: Mapped[Language] = relationship(
        "Language",
        primaryjoin=language_id == Language.id,
        uselist=False,
        backref="translations",
        lazy="joined",
    )
