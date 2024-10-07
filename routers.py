from typing import Any

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import session
from database.models import WordModel, WordValue
from database.repository import Dictionary

dictionary = FastAPI()


@dictionary.get("/words/{language}/", response_model=list[WordValue])
async def get_all_words_of_language(language: str, db: AsyncSession = Depends(session)) -> Any:
    return await Dictionary.get_all_words(session=db, language=language)


@dictionary.get("/word/{base}/{word}/in/{lang}/", response_model=WordModel)
async def translate(word: str, lang: str, base: str, db: AsyncSession = Depends(session)) -> Any:
    return await Dictionary.get_translation(session=db, to=lang, language=base, value=word)
