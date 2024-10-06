from typing import Any

from fastapi import Depends, FastAPI
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import session
from database.repository import Dictionary

dictionary = FastAPI()


class Language(BaseModel):  # type: ignore
    name: str


class Word(BaseModel):  # type: ignore
    value: str
    language: Language


@dictionary.get("/word/{base}/{word}/in/{lang}/", response_model=Word)
async def translate(word: str, lang: str, base: str, db: AsyncSession = Depends(session)) -> Any:
    return await Dictionary.get_translation(session=db, to=lang, language=base, value=word)
