from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_TAXI = "TAXI"
LHR_TO_HILTON_TAXI_ROUTE_IDS = {"taxi009", "taxi010"}
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Runtime cache
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path for the task."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "booking", f"task_{task_id:02d}")


def _read_runtime_json(
    task_id: int, filename: str, device_id: str | None, backup_dir: str | None
):
    """Read runtime JSON file from device or backup directory."""
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
    """Convert value to list or return empty list."""
    return value if isinstance(value, list) else []


def _orders(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all orders from runtime data."""
    payload = _read_runtime_json(task_id, ORDERS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching the predicate."""
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
    """Find the latest order matching the given criteria."""
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
    """Convert timestamp in milliseconds to local datetime."""
    try:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
    except Exception:
        return None


def _to_local_date(timestamp_ms):
    """Convert timestamp in milliseconds to local date."""
    dt = _to_local_datetime(timestamp_ms)
    return dt.date() if dt is not None else None


def _matches_local_date(timestamp_ms, target_date) -> bool:
    """Check if timestamp matches the target date in local timezone."""
    return _to_local_date(timestamp_ms) == target_date


def _today_local_date():
    """Get today's date in local timezone."""
    return datetime.now(SHANGHAI_TZ).date()


def verify_book_taxi_lhr_to_hilton_now(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify that a taxi from LHR to Hilton has been booked for today.

    Task 15: Book a taxi from London Heathrow Airport (LHR) to Hilton hotel
    for today (now).

    Success criteria:
    - An ACTIVE order exists
    - Order type is TAXI
    - Item ID is one of the LHR to Hilton taxi routes (taxi009 or taxi010)
    - Start date matches today's date
    """
    task_id = 15

    # Find the latest taxi order matching the route
    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_TAXI,
        item_ids=LHR_TO_HILTON_TAXI_ROUTE_IDS,
        status="ACTIVE",
    )

    # Verify order exists and start date is today
    return bool(order and _matches_local_date(order.get("startDate"), _today_local_date()))


if __name__ == "__main__":
    print(verify_book_taxi_lhr_to_hilton_now())
