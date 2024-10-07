from pydantic import BaseModel, ConfigDict


class LanguageModel(BaseModel):  # type: ignore
    model_config = ConfigDict(from_attributes=True)
    name: str


class WordModel(BaseModel):  # type: ignore
    model_config = ConfigDict(from_attributes=True)
    value: str
    language: LanguageModel


class WordValue(BaseModel):  # type: ignore
    model_config = ConfigDict(from_attributes=True)
