from database.models import WordModel
from database.schemas import Word

from .fixtures import eng, hello_word  # noqa


def test_word_model(hello_word: Word) -> None:
    model = WordModel.model_validate(hello_word)
    assert hasattr(model, "value")
    assert hasattr(model, "language")
