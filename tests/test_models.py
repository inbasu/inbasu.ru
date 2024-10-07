from database.models import WordModel

from .fixtures import eng, hello_word  # noqa


def test_word_model(hello_word):
    model = WordModel.model_validate(hello_word)
    assert hasattr(model, "value")
    assert hasattr(model, "language")
