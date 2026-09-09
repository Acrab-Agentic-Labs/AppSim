from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_ATTRACTION = "ATTRACTION"
PARIS_MOST_EXPENSIVE_VIP_TICKET_ID = "tkt003"
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path for the given task."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "booking", f"task_{task_id:02d}")


def _read_runtime_json(task_id: int, filename: str, device_id: str | None, backup_dir: str | None):
    """Read JSON data from device or backup directory with caching."""
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
    """Convert value to list if it's a list, otherwise return empty list."""
    return value if isinstance(value, list) else []


def _orders(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all orders from the device or backup."""
    payload = _read_runtime_json(task_id, ORDERS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching the predicate."""
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _to_local_datetime(timestamp_ms) -> datetime | None:
    """Convert millisecond timestamp to local datetime in Shanghai timezone."""
    try:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
    except Exception:
        return None


def _to_local_date(timestamp_ms) -> date | None:
    """Convert millisecond timestamp to local date in Shanghai timezone."""
    dt = _to_local_datetime(timestamp_ms)
    return dt.date() if dt is not None else None


def _matches_local_date(timestamp_ms, target_date: date) -> bool:
    """Check if timestamp matches the target date in local timezone."""
    return _to_local_date(timestamp_ms) == target_date


def _day_after_tomorrow_local_date() -> date:
    """Get the date for day after tomorrow in local timezone."""
    today = datetime.now(SHANGHAI_TZ).date()
    return today + timedelta(days=2)


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


def verify_book_paris_most_expensive_vip_ticket(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify that the most expensive VIP ticket in Paris has been booked
    for the day after tomorrow.

    Task 18: Book the most expensive VIP ticket in Paris for the day after tomorrow.

    Args:
        result: Optional result data (not used in this verification)
        device_id: Device identifier for reading from device
        backup_dir: Backup directory for reading from backup
        **kwargs: Additional keyword arguments (ignored)

    Returns:
        bool: True if the verification passes, False otherwise
    """
    task_id = 18
    day_after_tomorrow = _day_after_tomorrow_local_date()

    # Find the latest order for the Paris most expensive VIP ticket
    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_ATTRACTION,
        item_ids={PARIS_MOST_EXPENSIVE_VIP_TICKET_ID},
        status="ACTIVE",
    )

    # Verify the order exists and the start date matches day after tomorrow
    return bool(order and _matches_local_date(order.get("startDate"), day_after_tomorrow))


if __name__ == "__main__":
    print(verify_book_paris_most_expensive_vip_ticket())

