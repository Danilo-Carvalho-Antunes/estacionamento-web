import os
from dataclasses import dataclass
from datetime import datetime, time
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


@dataclass
class _Lot:
    id: int = 1
    contractor_id: int = 1
    name: str = "Lote Teste"
    open_at: time = time(0, 0)
    close_at: time = time(23, 59)
    capacity: int = 100


@dataclass
class _Pricing:
    id: int = 1
    parking_lot_id: int = 1
    name: str = "default"
    fraction_minutes: int = 15
    fraction_rate: Decimal = Decimal("2.50")
    hourly_rate: Decimal = Decimal("8.00")
    daily_rate: Decimal = Decimal("30.00")
    nightly_rate: Decimal = Decimal("20.00")


@dataclass
class _Event:
    id: int = 1
    parking_lot_id: int = 1
    name: str = "Show"
    starts_at: datetime = datetime(2024, 12, 1, 9, 0, 0)
    ends_at: datetime = datetime(2024, 12, 1, 18, 0, 0)
    price: Decimal = Decimal("99.99")


@pytest.fixture(autouse=True)
def patch_pricing_repos(monkeypatch):
    import app.services.pricing as pricing_mod

    class FakeLotRepo:
        def __init__(self, db):
            pass

        def get(self, lot_id: int):
            return _Lot(id=lot_id)

    class FakePricingRepo:
        def __init__(self, db):
            pass

        def get_for_lot(self, lot_id: int):
            return _Pricing(parking_lot_id=lot_id)

    class FakeEventRepo:
        def __init__(self, db):
            pass

        def find_overlapping(self, lot_id: int, start_at: datetime, end_at: datetime):
            return None  # default: no event

    monkeypatch.setattr(pricing_mod, "ParkingLotRepository", FakeLotRepo)
    monkeypatch.setattr(pricing_mod, "PricingProfileRepository", FakePricingRepo)
    monkeypatch.setattr(pricing_mod, "EventRepository", FakeEventRepo)


async def test_quote_nightly_rate(async_client):
    r = await async_client.get(
        "/v1/lots/1/quote",
        params={"start_at": "2024-12-01T22:00:00", "end_at": "2024-12-01T23:00:00"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["charged_value"] == "20.00"
    assert body["charging_type"] == "nightly"


async def test_quote_daily_rate(async_client):
    # > 9 hours triggers daily
    r = await async_client.get(
        "/v1/lots/1/quote",
        params={"start_at": "2024-12-01T08:00:00", "end_at": "2024-12-01T18:30:00"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["charged_value"] == "30.00"
    assert body["charging_type"] == "daily"


async def test_quote_event_override(monkeypatch, async_client):
    import app.services.pricing as pricing_mod

    class EventRepoWithEvent:
        def __init__(self, db):
            pass

        def find_overlapping(self, lot_id: int, start_at: datetime, end_at: datetime):
            return _Event(parking_lot_id=lot_id)

    # Override only for this test
    monkeypatch.setattr(pricing_mod, "EventRepository", EventRepoWithEvent)

    r = await async_client.get(
        "/v1/lots/1/quote",
        params={"start_at": "2024-12-01T10:00:00", "end_at": "2024-12-01T12:00:00"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["charged_value"] == "99.99"
    assert body["charging_type"] == "event"


async def test_quote_fraction_rounding(async_client):
    # 16 minutes with 15-min fraction -> 2 intervals * 2.50 = 5.00
    r = await async_client.get(
        "/v1/lots/1/quote",
        params={"start_at": "2024-12-01T10:00:00", "end_at": "2024-12-01T10:16:00"},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["charged_value"] == "5.00"
    assert body["charging_type"] == "fraction"
