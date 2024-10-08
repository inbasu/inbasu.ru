from typing import Any

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import session
from database.models import WordModel, WordValue
from database.repository import Words
from database.schemas import Language

dictionary = FastAPI()


@dictionary.get("/words/{language}/", response_model=list[WordValue])
async def get_all_words_of_language(language: str, db: AsyncSession = Depends(session)) -> Any:
    return await Words(db).get_all_words(language=Language(name=language))


@dictionary.get("/word/{base}/{word}/in/{lang}/", response_model=WordModel)
async def translate(word: str, lang: str, base: str, db: AsyncSession = Depends(session)) -> Any:
    return await Words(db).get_translation(to=lang, language=base, value=word)
