from __future__ import annotations

import os
from datetime import timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_CAR_RENTAL = "CAR_RENTAL"
HKG_CAR_IDS = {"car013", "car014", "car015", "car016"}
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path for the task."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "booking", f"task_{task_id:02d}")


def _read_runtime_json(task_id: int, filename: str, device_id: str | None, backup_dir: str | None):
    """Read runtime JSON file with caching."""
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
    """Get all orders from the runtime data."""
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
    """Find the latest order matching the criteria."""
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


def _to_local_datetime(timestamp_ms):
    """Convert timestamp to local datetime."""
    from datetime import datetime
    try:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
    except Exception:
        return None


def _to_local_date(timestamp_ms):
    """Convert timestamp to local date."""
    dt = _to_local_datetime(timestamp_ms)
    return dt.date() if dt is not None else None


def _matches_local_date(timestamp_ms, target_date) -> bool:
    """Check if timestamp matches the target date in local timezone."""
    return _to_local_date(timestamp_ms) == target_date


def _matches_local_slot(timestamp_ms, target_date, hour: int, minute: int, tolerance_minutes: int = 90) -> bool:
    """Check if timestamp matches the target date and time slot within tolerance."""
    from datetime import datetime
    actual = _to_local_datetime(timestamp_ms)
    if actual is None or actual.date() != target_date:
        return False
    target = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=SHANGHAI_TZ)
    return abs((actual - target).total_seconds()) <= tolerance_minutes * 60


def _today_local_date():
    """Get today's date in local timezone."""
    from datetime import datetime
    return datetime.now(SHANGHAI_TZ).date()


def _day_after_tomorrow_local_date():
    """Get the date for the day after tomorrow in local timezone."""
    from datetime import timedelta
    return _today_local_date() + timedelta(days=2)


def verify_book_hkg_car_with_child_seat(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 13: Book a car rental in Hong Kong with a child seat.

    This task checks if:
    - A car rental order exists for one of the HKG car IDs
    - The order is ACTIVE
    - The start date is the day after tomorrow
    - The pickup time is around 12:00 (noon) with 90 minutes tolerance
    - The car includes a child seat (checked via item name)

    Args:
        result: Task execution result (unused in this verification)
        device_id: Device ID for reading runtime data
        backup_dir: Backup directory path for runtime data
        **kwargs: Additional keyword arguments (unused)

    Returns:
        bool: True if the verification passes, False otherwise
    """
    task_id = 13
    day_after_tomorrow = _day_after_tomorrow_local_date()

    # Find the latest car rental order for HKG cars with ACTIVE status
    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_CAR_RENTAL,
        item_ids=HKG_CAR_IDS,
        status="ACTIVE",
    )

    # Extract item name and check for child seat
    item_name = str(order.get("itemName", "")) if order else ""

    # Verify all conditions:
    # 1. Order exists
    # 2. Start date is day after tomorrow
    # 3. Start time is around 12:00 (noon)
    # 4. Item name contains "child seat"
    return bool(
        order
        and _matches_local_date(order.get("startDate"), day_after_tomorrow)
        and _matches_local_slot(order.get("startDate"), day_after_tomorrow, 12, 0)
        and "child seat" in item_name.lower()
    )


if __name__ == "__main__":
    print(verify_book_hkg_car_with_child_seat())

