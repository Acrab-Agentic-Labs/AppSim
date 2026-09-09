from __future__ import annotations

import os
from datetime import date, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_STAY = "STAY"
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Cache for runtime data
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


def _to_local_date(timestamp_ms) -> date | None:
    from datetime import datetime

    try:
        dt = datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
        return dt.date() if dt is not None else None
    except Exception:
        return None


def _matches_local_date(timestamp_ms, target_date: date) -> bool:
    return _to_local_date(timestamp_ms) == target_date


def _today_local_date() -> date:
    from datetime import datetime

    return datetime.now(SHANGHAI_TZ).date()


def _tomorrow_local_date() -> date:
    return _today_local_date() + timedelta(days=1)


def verify_book_highest_rated_london_stay_tomorrow(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 2: Book the highest rated hotel in London for tomorrow.

    This checks if there's an active order for hotel 'htl001' with a start date
    matching tomorrow's date.
    """
    task_id = 2
    tomorrow = _tomorrow_local_date()

    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_STAY,
        item_ids={"htl001"},
        status="ACTIVE",
    )
    return bool(order and _matches_local_date(order.get("startDate"), tomorrow))


if __name__ == "__main__":
    print(verify_book_highest_rated_london_stay_tomorrow())

