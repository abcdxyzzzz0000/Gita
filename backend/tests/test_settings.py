import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def _register_and_get_headers(client: AsyncClient) -> dict:
    resp = await client.post(
        "/api/auth/register",
        json={"email": "settingsuser@test.com", "password": "password123"},
    )
    token = resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


async def test_get_settings_unauthenticated(client: AsyncClient):
    response = await client.get("/api/settings")
    assert response.status_code == 401


async def test_get_settings(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.get("/api/settings", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["notification_enabled"] is True
    assert data["notification_time"] == "08:00"


async def test_update_settings(client: AsyncClient):
    headers = await _register_and_get_headers(client)
    response = await client.put(
        "/api/settings",
        json={"notification_enabled": False, "notification_time": "20:00"},
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["notification_enabled"] is False
    assert data["notification_time"] == "20:00"


async def test_audio_not_found(client: AsyncClient):
    response = await client.get("/api/shlokas/00000000-0000-0000-0000-000000000000/audio")
    assert response.status_code == 404
