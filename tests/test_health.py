import os

# Ensure Settings() can be constructed during import by providing a dummy DB_URL
os.environ.setdefault("DB_URL", "sqlite+pysqlite:///:memory:")

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        yield ac


async def test_health_ok(async_client):
    resp = await async_client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}
