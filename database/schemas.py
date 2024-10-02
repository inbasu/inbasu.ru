from sqlalchemy.orm import Mapped, mapped_column

from .connection import Base


class Word(Base):
    __tablename__ = "words"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
