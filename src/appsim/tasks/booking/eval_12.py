"""Task 12: Book LHR car until next Monday - Evaluation module."""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_CAR_RENTAL = "CAR_RENTAL"
LHR_CAR_ID = "car004"
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build backup directory path for task data."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "booking", f"task_{task_id:02d}")


def _read_runtime_json(
    task_id: int,
    filename: str,
    device_id: str | None,
    backup_dir: str | None,
):
    """Read and cache runtime JSON data from device or backup."""
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
    """Convert value to list if it is a list, otherwise return empty list."""
    return value if isinstance(value, list) else []


def _orders(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
) -> list[dict]:
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
    """Find the latest order matching the specified criteria."""
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
    """Convert milliseconds timestamp to local datetime."""
    try:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
    except Exception:
        return None


def _to_local_date(timestamp_ms) -> date | None:
    """Convert milliseconds timestamp to local date."""
    dt = _to_local_datetime(timestamp_ms)
    return dt.date() if dt is not None else None


def _matches_any_local_date(timestamp_ms, target_dates: set[date]) -> bool:
    """Check if timestamp matches any of the target dates."""
    actual = _to_local_date(timestamp_ms)
    return actual in target_dates if actual is not None else False


def _today_local_date() -> date:
    """Get today's date in local timezone."""
    return datetime.now(SHANGHAI_TZ).date()


def _next_weekday_candidates(weekday: int) -> set[date]:
    """Get candidate dates for the next occurrence of a weekday."""
    today = _today_local_date()
    delta = (weekday - today.weekday()) % 7
    if delta == 0:
        delta = 7
    return {today + timedelta(days=delta), today + timedelta(days=delta + 7)}


def verify_book_lhr_car_until_next_monday(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify that a car rental at LHR has been booked until next Monday.

    Task 12: Book LHR car until next Monday
    Checks for an active car rental order for the LHR car (car004)
    with an end date matching next Monday (weekday 0).
    """
    task_id = 12
    next_monday_candidates = _next_weekday_candidates(0)  # Monday is weekday 0

    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_CAR_RENTAL,
        item_ids={LHR_CAR_ID},
        status="ACTIVE",
    )

    return bool(
        order and _matches_any_local_date(order.get("endDate"), next_monday_candidates)
    )


if __name__ == "__main__":
    print(verify_book_lhr_car_until_next_monday())

