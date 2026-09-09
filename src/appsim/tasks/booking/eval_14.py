from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_CAR_RENTAL = "CAR_RENTAL"
CHEAPEST_HKG_COMFORT_SEDAN_ID = "car015"
SHANGHAI_TZ = timezone(timedelta(hours=8))

_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "booking", f"task_{task_id:02d}")


def _read_runtime_json(task_id: int, filename: str, device_id: str | None, backup_dir: str | None):
    cache_key = (task_id, filename, device_id, backup_dir)
    if cache_key not in _RUNTIME_CACHE:
        _RUNTIME_CACHE[cache_key] = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{filename}",
            backup_dir=_build_backup_dir(task_id, backup_dir),
        )
    return _RUNTIME_CACHE[cache_key]


def _as_list(value) -> list:
    return value if isinstance(value, list) else []


def _orders(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, ORDERS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _latest_order_by_items(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    order_type: str | None = None,
    item_ids: set[str] | None = None,
    status: str | None = None,
) -> dict | None:
    allowed_items = {str(item_id) for item_id in (item_ids or set()) if item_id}

    def predicate(order: dict) -> bool:
        if order_type and str(order.get("orderType", "")) != order_type:
            return False
        if status and str(order.get("status", "")) != status:
            return False
        if allowed_items and str(order.get("itemId", "")) not in allowed_items:
            return False
        return True

    return _find_latest(_orders(task_id, device_id, backup_dir), predicate)


def _to_local_datetime(timestamp_ms) -> datetime | None:
    try:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
    except Exception:
        return None


def _to_local_date(timestamp_ms) -> date | None:
    dt = _to_local_datetime(timestamp_ms)
    return dt.date() if dt is not None else None


def _matches_local_date(timestamp_ms, target_date: date) -> bool:
    return _to_local_date(timestamp_ms) == target_date


def _matches_local_slot(timestamp_ms, target_date: date, hour: int, minute: int, tolerance_minutes: int = 90) -> bool:
    actual = _to_local_datetime(timestamp_ms)
    if actual is None or actual.date() != target_date:
        return False
    target = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=SHANGHAI_TZ)
    return abs((actual - target).total_seconds()) <= tolerance_minutes * 60


def _today_local_date() -> date:
    return datetime.now(SHANGHAI_TZ).date()


def _day_after_tomorrow_local_date() -> date:
    return _today_local_date() + timedelta(days=2)


def verify_book_cheapest_comfort_sedan_at_hkg(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 14: Book the cheapest comfort sedan at HKG airport.

    Success criteria:
    - Order exists for car rental
    - Item ID is car015 (cheapest HKG comfort sedan)
    - Status is ACTIVE
    - Start date matches day after tomorrow
    - Start time is around 12:00 (within 90 minutes tolerance)
    """
    task_id = 14
    day_after_tomorrow = _day_after_tomorrow_local_date()

    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_CAR_RENTAL,
        item_ids={CHEAPEST_HKG_COMFORT_SEDAN_ID},
        status="ACTIVE",
    )

    return bool(
        order
        and _matches_local_date(order.get("startDate"), day_after_tomorrow)
        and _matches_local_slot(order.get("startDate"), day_after_tomorrow, 12, 0)
    )


if __name__ == "__main__":
    print(verify_book_cheapest_comfort_sedan_at_hkg())

