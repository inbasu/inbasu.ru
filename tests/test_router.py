import pytest
from httpx import ASGITransport, AsyncClient

from routers import dictionary

from .fixtures import create_table, create_word_hello, drop_table  # noqa


@pytest.mark.asyncio(loop_scope="session")
async def test_translate_word() -> None:
    async with AsyncClient(transport=ASGITransport(app=dictionary), base_url="http://test") as client:
        response = await client.get("/word/en/hello/in/fr/")
    assert response.json().get("value", "") == "bonjour"
    assert response.json().get("language", {}).get("name", "") == "fr"
