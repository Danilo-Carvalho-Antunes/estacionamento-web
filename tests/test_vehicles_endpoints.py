import os
from dataclasses import dataclass

import pytest
from httpx import AsyncClient, ASGITransport

# Ensure Settings() can be constructed during import by providing a dummy DB_URL
os.environ.setdefault("DB_URL", "sqlite+pysqlite:///:memory:")

from app.main import app  # noqa: E402

pytestmark = pytest.mark.asyncio


@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://testserver") as ac:
        yield ac


@dataclass
class _Vehicle:
    id: int
    plate: str
    owner_name: str | None = None


@pytest.fixture(autouse=True)
def patch_vehicle_repo(monkeypatch):
    import app.api.v1.vehicles as mod

    class FakeVehicleRepo:
        def __init__(self, db):
            pass

        def list(self):
            return [_Vehicle(1, "ABC1D23"), _Vehicle(2, "XYZ9Z99", owner_name="John Doe")]

        def get(self, vehicle_id: int):
            if vehicle_id == 1:
                return _Vehicle(1, "ABC1D23")
            return None

    monkeypatch.setattr(mod, "VehicleRepository", FakeVehicleRepo)


async def test_list_vehicles_ok(async_client):
    r = await async_client.get("/v1/vehicles/")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) == 2
    assert data[0]["plate"] == "ABC1D23"
    assert data[1]["owner_name"] == "John Doe"


async def test_get_vehicle_ok(async_client):
    r = await async_client.get("/v1/vehicles/1")
    assert r.status_code == 200
    body = r.json()
    assert body["id"] == 1 and body["plate"] == "ABC1D23"


async def test_get_vehicle_not_found(async_client):
    r = await async_client.get("/v1/vehicles/999")
    assert r.status_code == 404
    body = r.json()
    assert body["detail"] == "Vehicle not found"
