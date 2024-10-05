
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from database.connection import session
from database.repository import Dictionary

dictionary = FastAPI()


@dictionary.get("/word/{base}/{word}/in/{lang}/")
async def translate(word: str, lang: str, base: str, db: AsyncSession = Depends(session)):
    return await Dictionary.get_translation(session=db, to=lang, language=base, value=word)
