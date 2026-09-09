"""
Task 6: Book again for last stay with no end room note.

Verification logic for booking task 6:
- Checks for a STAY_BOOK_AGAIN_PREPARED action
- Verifies an active order for hotel htl001
- Confirms the booking is for tomorrow
"""

from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME = "runtime_account_action_signals.json"
ORDER_TYPE_STAY = "STAY"
ACTION_STAY_BOOK_AGAIN_PREPARED = "STAY_BOOK_AGAIN_PREPARED"
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


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _orders(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, ORDERS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _account_action_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _latest_account_action(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    action_type: str,
    field_name: str | None = None,
) -> dict | None:
    def predicate(signal: dict) -> bool:
        if str(signal.get("actionType", "")) != action_type:
            return False
        if field_name is not None:
            extra = _as_dict(signal.get("extra"))
            if str(extra.get("field", "")) != field_name:
                return False
        return True

    return _find_latest(_account_action_signals(task_id, device_id, backup_dir), predicate)


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


def _today_local_date() -> date:
    return datetime.now(SHANGHAI_TZ).date()


def _tomorrow_local_date() -> date:
    return _today_local_date() + timedelta(days=1)


def verify_book_again_last_stay_with_no_end_room_note(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 6: Book again for last stay with no end room note.

    Checks:
    1. A STAY_BOOK_AGAIN_PREPARED action was triggered
    2. An ACTIVE order exists for hotel htl001
    3. The booking start date is tomorrow
    """
    task_id = 6
    tomorrow = _tomorrow_local_date()

    # Check for book again prepared action
    prepared = _latest_account_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_STAY_BOOK_AGAIN_PREPARED,
    )

    # Check for active order for htl001
    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_STAY,
        item_ids={"htl001"},
        status="ACTIVE",
    )

    # Verify all conditions are met
    return bool(prepared and order and _matches_local_date(order.get("startDate"), tomorrow))


if __name__ == "__main__":
    print(verify_book_again_last_stay_with_no_end_room_note())


