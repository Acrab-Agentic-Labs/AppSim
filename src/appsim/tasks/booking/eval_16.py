from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDER_TYPE_TAXI = "TAXI"
LHR_TO_HILTON_TAXI_ROUTE_IDS = {"taxi009", "taxi010"}
SHANGHAI_TZ = timezone(timedelta(hours=8))
ORDERS_FILE_NAME = "orders.json"

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path for a given task."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "booking", f"task_{task_id:02d}")


def _read_runtime_json(
    task_id: int, filename: str, device_id: str | None, backup_dir: str | None
):
    """Read runtime JSON data with caching."""
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
    """Ensure value is a list."""
    return value if isinstance(value, list) else []


def _orders(
    task_id: int, device_id: str | None, backup_dir: str | None
) -> list[dict]:
    """Get all orders from runtime data."""
    payload = _read_runtime_json(task_id, ORDERS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching a predicate."""
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
    """Get the latest order matching the specified criteria."""
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


def _to_local_date(timestamp_ms) -> date | None:
    """Convert timestamp in milliseconds to local date."""
    dt = _to_local_datetime(timestamp_ms)
    return dt.date() if dt is not None else None


def _matches_local_slot(
    timestamp_ms, target_date: date, hour: int, minute: int, tolerance_minutes: int = 90
) -> bool:
    """Check if timestamp matches a specific time slot on a target date."""
    actual = _to_local_datetime(timestamp_ms)
    if actual is None or actual.date() != target_date:
        return False
    target = datetime(
        target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=SHANGHAI_TZ
    )
    return abs((actual - target).total_seconds()) <= tolerance_minutes * 60


def _today_local_date() -> date:
    """Get today's date in local timezone."""
    return datetime.now(SHANGHAI_TZ).date()


def _tomorrow_local_date() -> date:
    """Get tomorrow's date in local timezone."""
    return _today_local_date() + timedelta(days=1)


def _day_after_tomorrow_local_date() -> date:
    """Get the day after tomorrow's date in local timezone."""
    return _today_local_date() + timedelta(days=2)


def verify_book_round_trip_taxi_lhr_hilton_and_return(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 16: Book a round-trip taxi from LHR to Hilton.

    The task expects:
    - A taxi order with route IDs in LHR_TO_HILTON_TAXI_ROUTE_IDS
    - Status: ACTIVE
    - Start time: tomorrow at 12:00 (noon)
    - End time: day after tomorrow at 8:00 (morning)
    """
    task_id = 16
    tomorrow = _tomorrow_local_date()
    day_after_tomorrow = _day_after_tomorrow_local_date()

    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_TAXI,
        item_ids=LHR_TO_HILTON_TAXI_ROUTE_IDS,
        status="ACTIVE",
    )

    return bool(
        order
        and _matches_local_slot(order.get("startDate"), tomorrow, 12, 0)
        and _matches_local_slot(order.get("endDate"), day_after_tomorrow, 8, 0)
    )


if __name__ == "__main__":
    print(verify_book_round_trip_taxi_lhr_hilton_and_return())

