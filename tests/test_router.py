import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from routers import dictionary

from .fixtures import create_table, create_word_hello, drop_table  # noqa


@pytest_asyncio.fixture(scope="session")
async def client() -> AsyncClient:
    return AsyncClient(transport=ASGITransport(app=dictionary), base_url="http://test")


@pytest.mark.asyncio(loop_scope="session")
async def test_translate_word(client: AsyncClient) -> None:
    response = await client.get("/word/en/hello/in/fr/")
    assert response.json().get("value", "") == "bonjour"
    assert response.json().get("language", {}).get("name", "") == "fr"


@pytest.mark.asyncio(loop_scope="session")
async def test_get_eng_words(client: AsyncClient) -> None:
    response = await client.get("/words/en/")
    assert len(response.json()) == 2
