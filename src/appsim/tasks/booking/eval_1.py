from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_STAY = "STAY"
LONDON_HOTEL_IDS = {"htl001", "htl016", "htl017", "htl018"}
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


# Helper functions
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


def _int_value(value, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _to_local_datetime(timestamp_ms) -> datetime | None:
    try:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
    except Exception:
        return None


def _to_local_date(timestamp_ms) -> date | None:
    dt = _to_local_datetime(timestamp_ms)
    return dt.date() if dt is not None else None


def _matches_any_local_date(timestamp_ms, target_dates: set[date]) -> bool:
    actual = _to_local_date(timestamp_ms)
    return actual in target_dates if actual is not None else False


def _today_local_date() -> date:
    return datetime.now(SHANGHAI_TZ).date()


def _next_weekday_candidates(weekday: int) -> set[date]:
    """Calculate the next occurrence(s) of a given weekday.

    Args:
        weekday: Target day of week (0=Monday, 5=Saturday, 6=Sunday)

    Returns:
        Set of two possible dates for the next occurrence of the weekday
    """
    today = _today_local_date()
    delta = (weekday - today.weekday()) % 7
    if delta == 0:
        delta = 7
    return {today + timedelta(days=delta), today + timedelta(days=delta + 7)}


def verify_book_london_stay_next_saturday(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """Verify that a London hotel stay for 2 guests was booked for next Saturday.

    This function checks if:
    1. An order exists for a London hotel (htl001, htl016, htl017, or htl018)
    2. The order is of type STAY and has status ACTIVE
    3. The guest count is exactly 2
    4. The start date matches next Saturday (allowing for flexibility in week selection)

    Args:
        result: Task execution result (not used in this verification)
        device_id: Device identifier for retrieving order data
        backup_dir: Backup directory path for data retrieval
        **kwargs: Additional keyword arguments (unused)

    Returns:
        bool: True if all verification conditions are met, False otherwise
    """
    task_id = 1
    next_saturday_candidates = _next_weekday_candidates(5)  # 5 = Saturday

    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_STAY,
        item_ids=LONDON_HOTEL_IDS,
        status="ACTIVE",
    )

    return bool(
        order
        and _int_value(order.get("guestCount")) == 2
        and _matches_any_local_date(order.get("startDate"), next_saturday_candidates)
    )


if __name__ == "__main__":
    print(verify_book_london_stay_next_saturday())

