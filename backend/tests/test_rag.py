import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_get_shloka_detail_not_found(client: AsyncClient):
    response = await client.get("/api/shlokas/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


async def test_semantic_search_short_query(client: AsyncClient):
    response = await client.get("/api/search/semantic", params={"q": "ab"})
    assert response.status_code == 422  # min_length=3


async def test_semantic_search_empty_index(client: AsyncClient):
    """When no FAISS index exists, semantic search returns empty results."""
    response = await client.get("/api/search/semantic", params={"q": "peace and calm"})
    assert response.status_code == 200
    assert response.json() == []
