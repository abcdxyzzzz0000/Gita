import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def test_register_success(client: AsyncClient):
    response = await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"


async def test_register_duplicate_email(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password456"},
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]


async def test_register_short_password(client: AsyncClient):
    response = await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "short"},
    )
    assert response.status_code == 422


async def test_login_success(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "password123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"


async def test_login_wrong_password(client: AsyncClient):
    await client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "password123"},
    )
    response = await client.post(
        "/api/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401


async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/api/auth/login",
        json={"email": "nobody@example.com", "password": "password123"},
    )
    assert response.status_code == 401
