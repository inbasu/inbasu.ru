from typing import List

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .connection import Base

translations = Table(
    "translations",
    Base.metadata,
    Column("left_id", ForeignKey("words.id"), primary_key=True),
    Column("right_id", ForeignKey("words.id"), primary_key=True),
)


class Language(Base):
    __tablename__ = "languages"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(3), unique=True)


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()
    language_id: Mapped[int] = mapped_column(ForeignKey("languages.id"))
    translation: Mapped[List["Word"]] = relationship(
        secondary=translations,
        primaryjoin=id == translations.c.left_id,
        secondaryjoin=id == translations.c.right_id,
        lazy="joined",
    )

    language: Mapped[Language] = relationship(
        "Language", primaryjoin=language_id == Language.id, uselist=False, backref="translations", lazy="joined"
    )
