import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def _register_and_get_headers(client: AsyncClient) -> dict:
    resp = await client.post(
        "/api/auth/register",
        json={"email": "progressuser@test.com", "password": "password123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_record_progress(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.post(
        "/api/progress",
        json={"chapter": 2, "shloka_number": 47},
        headers=headers,
    )
    assert response.status_code == 201


async def test_get_progress(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.get("/api/progress", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "chapter_progress" in data
    assert "total_read" in data
    assert "streak" in data
