import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def _register_and_get_headers(client: AsyncClient) -> dict:
    resp = await client.post(
        "/api/auth/register",
        json={"email": "profileuser@test.com", "password": "password123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_get_profile_unauthenticated(client: AsyncClient):
    response = await client.get("/api/profile")
    assert response.status_code == 401


async def test_get_profile(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.get("/api/profile", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert "stats" in data
    assert data["user"]["email"] == "profileuser@test.com"
    assert data["stats"]["bookmark_count"] == 0
    assert data["stats"]["shlokas_read"] == 0
