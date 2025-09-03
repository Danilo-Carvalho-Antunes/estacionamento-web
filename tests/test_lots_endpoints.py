import os
from datetime import time, datetime
from decimal import Decimal

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


class _Lot:
    def __init__(self, id: int = 1):
        self.id = id
        self.contractor_id = 1
        self.name = "Lote A"
        self.open_at = time(8, 0)
        self.close_at = time(20, 0)
        self.capacity = 100


class _Pricing:
    def __init__(self):
        self.id = 1
        self.parking_lot_id = 1
        self.name = "default"
        self.fraction_minutes = 15
        self.fraction_rate = Decimal("2.50")
        self.hourly_rate = Decimal("8.00")
        self.daily_rate = Decimal("30.00")
        self.nightly_rate = Decimal("20.00")


class _PriceResult:
    def __init__(self, value: str, typ: str):
        self.charged_value = Decimal(value)
        self.charging_type = typ


@pytest.fixture(autouse=True)
def patch_repositories(monkeypatch):
    import app.api.v1.lots as lots_mod

    class FakeLotRepo:
        def __init__(self, db):
            pass

        def list(self):
            return [_Lot(1), _Lot(2)]

        def get(self, lot_id: int):
            return _Lot(lot_id)

    class FakePricingRepo:
        def __init__(self, db):
            pass

        def get_for_lot(self, lot_id: int):
            return _Pricing()

    def fake_calc_price(db, lot_id: int, start_at: datetime, end_at: datetime):
        return _PriceResult("10.00", "hourly")

    monkeypatch.setattr(lots_mod, "ParkingLotRepository", FakeLotRepo)
    monkeypatch.setattr(lots_mod, "PricingProfileRepository", FakePricingRepo)
    monkeypatch.setattr(lots_mod, "calculate_price", fake_calc_price)


async def test_list_lots_ok(async_client):
    r = await async_client.get("/v1/lots/")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list) and len(data) == 2
    assert data[0]["name"] == "Lote A"


async def test_get_lot_ok(async_client):
    r = await async_client.get("/v1/lots/1")
    assert r.status_code == 200
    assert r.json()["id"] == 1


async def test_get_pricing_ok(async_client):
    r = await async_client.get("/v1/lots/1/pricing")
    assert r.status_code == 200
    body = r.json()
    assert body["name"] == "default"
    assert body["hourly_rate"] == "8.00"


async def test_quote_ok(async_client):
    r = await async_client.get(
        "/v1/lots/1/quote",
        params={
            "start_at": "2024-12-01T10:00:00",
            "end_at": "2024-12-01T11:30:00",
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["charged_value"] == "10.00"
    assert body["charging_type"] == "hourly"
