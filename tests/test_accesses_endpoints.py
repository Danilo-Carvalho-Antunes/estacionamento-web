import os
from datetime import datetime, time, timedelta
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


class _Vehicle:
    def __init__(self, id: int, plate: str):
        self.id = id
        self.plate = plate
        self.owner_name = None


class _Access:
    def __init__(self, id: int, vehicle_id: int, parking_lot_id: int, start_at: datetime):
        self.id = id
        self.vehicle_id = vehicle_id
        self.parking_lot_id = parking_lot_id
        self.start_at = start_at
        self.end_at = None
        self.price = None
        self.status = "open"


class _PriceResult:
    def __init__(self, value: str, typ: str):
        self.charged_value = Decimal(value)
        self.charging_type = typ


@pytest.fixture(autouse=True)
def patch_repositories(monkeypatch):
    import app.api.v1.accesses as mod
    # Shared state across repo instances and requests within this test module
    shared = {
        "veh_seq": 1,
        "vehicles": {},  # plate -> _Vehicle
        "acc_seq": 1,
        "open": None,  # currently open _Access
    }

    class FakeLotRepo:
        def __init__(self, db):
            self._open_count = 0

        def get(self, lot_id: int):
            return _Lot(lot_id)

        def count_open_accesses(self, lot_id: int) -> int:
            return self._open_count

    class FakeVehicleRepo:
        def __init__(self, db):
            pass

        def get_by_plate(self, plate: str):
            return shared["vehicles"].get(plate)

        def create(self, vehicle):
            v = _Vehicle(shared["veh_seq"], vehicle.plate)
            shared["vehicles"][v.plate] = v
            shared["veh_seq"] += 1
            return v

    class FakeAccessRepo:
        def __init__(self, db):
            pass

        def find_open_by_vehicle(self, lot_id: int, vehicle_id: int):
            if (
                shared["open"]
                and shared["open"].parking_lot_id == lot_id
                and shared["open"].vehicle_id == vehicle_id
                and shared["open"].status == "open"
            ):
                return shared["open"]
            return None

        def create(self, access):
            a = _Access(shared["acc_seq"], access.vehicle_id, access.parking_lot_id, access.start_at)
            shared["open"] = a
            shared["acc_seq"] += 1
            return a

        def close(self, access, end_at: datetime, price):
            access.end_at = end_at
            access.price = price
            access.status = "closed"
            # reflect closure in shared state
            if shared["open"] and shared["open"].id == access.id:
                shared["open"] = access
            return access

    def fake_calc_price(db, lot_id: int, start_at: datetime, end_at: datetime):
        return _PriceResult("10.00", "hourly")

    monkeypatch.setattr(mod, "ParkingLotRepository", FakeLotRepo)
    monkeypatch.setattr(mod, "VehicleRepository", FakeVehicleRepo)
    monkeypatch.setattr(mod, "AccessRepository", FakeAccessRepo)
    monkeypatch.setattr(mod, "calculate_price", fake_calc_price)


async def test_enter_ok(async_client):
    r = await async_client.post(
        "/v1/lots/1/accesses/enter",
        json={"plate": "ABC1D23", "start_at": "2024-12-01T10:00:00"},
    )
    assert r.status_code == 201
    body = r.json()
    assert body["parking_lot_id"] == 1
    assert body["status"] == "open"


async def test_exit_ok(async_client):
    # First enter
    r1 = await async_client.post(
        "/v1/lots/1/accesses/enter",
        json={"plate": "ABC1D23", "start_at": "2024-12-01T10:00:00"},
    )
    assert r1.status_code == 201

    # Then exit
    r2 = await async_client.post(
        "/v1/lots/1/accesses/exit",
        json={"plate": "ABC1D23", "end_at": "2024-12-01T11:00:00"},
    )
    assert r2.status_code == 200
    body = r2.json()
    assert body["charged_value"] == "10.00"
    assert body["charging_type"] == "hourly"
