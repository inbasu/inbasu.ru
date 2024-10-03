from typing import List

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .connection import Base

translations = Table(
    "translations",
    Base.metadata,
    Column("left_id", ForeignKey("words.id"), primary_key=True),
    Column("right_id", ForeignKey("words.id"), primary_key=True),
)


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    lang: Mapped[str]
    translation: Mapped[List["Word"]] = relationship(
        secondary=translations,
        primaryjoin=id == translations.c.left_id,
        secondaryjoin=id == translations.c.right_id,
    )
