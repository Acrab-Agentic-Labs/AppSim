from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME = "runtime_account_action_signals.json"
ACTION_FUTURE_ORDERS_CANCELLED = "FUTURE_ORDERS_CANCELLED"
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


def _future_cancel_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [
        signal
        for signal in _account_action_signals(task_id, device_id, backup_dir)
        if str(signal.get("actionType", "")) == ACTION_FUTURE_ORDERS_CANCELLED
    ]


def _int_value(value, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _has_active_orders_after_cutoff(task_id: int, device_id: str | None, backup_dir: str | None, cutoff_millis: int) -> bool:
    for order in _orders(task_id, device_id, backup_dir):
        if str(order.get("status", "")) != "ACTIVE":
            continue
        if _int_value(order.get("startDate"), -1) > cutoff_millis:
            return True
    return False


def _latest_order(task_id: int, device_id: str | None, backup_dir: str | None, *, order_type: str | None = None, item_id: str | None = None) -> dict | None:
    def predicate(order: dict) -> bool:
        if order_type and str(order.get("orderType", "")) != order_type:
            return False
        if item_id and str(order.get("itemId", "")) != item_id:
            return False
        return True

    return _find_latest(_orders(task_id, device_id, backup_dir), predicate)


def _future_cancel_cutoff_millis(action_signal: dict) -> int | None:
    """Extract cutoff timestamp from cancel action signal."""
    extra = _as_dict(action_signal.get("extra"))
    cutoff_raw = extra.get("cutoffMillis")
    if cutoff_raw is None:
        return None
    try:
        return int(cutoff_raw)
    except Exception:
        return None


def verify_cancel_all_orders_after_next_month(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Task 25: Verify all future orders were cancelled after a cutoff date.

    Checks:
    - At least one successful cancel action exists
    - Cruise order (crs001) is cancelled
    - No active orders exist after the cutoff timestamp
    """
    task_id = 25

    cancel_actions = _future_cancel_actions(task_id, device_id, backup_dir)
    has_successful_cancel = any(
        _int_value(action.get("affectedOrderCount")) >= 1
        for action in cancel_actions
    )

    cutoff_candidates = [
        cutoff
        for cutoff in (_future_cancel_cutoff_millis(action) for action in cancel_actions)
        if cutoff is not None
    ]
    latest_cutoff = max(cutoff_candidates) if cutoff_candidates else None
    if latest_cutoff is None:
        return False

    cruise_order = _latest_order(task_id, device_id, backup_dir, item_id="crs001")
    cruise_cancelled = bool(
        cruise_order and str(cruise_order.get("status", "")) == "CANCELLED"
    )
    no_active_orders_after_cutoff = not _has_active_orders_after_cutoff(
        task_id,
        device_id,
        backup_dir,
        latest_cutoff,
    )
    return has_successful_cancel and cruise_cancelled and no_active_orders_after_cutoff


if __name__ == "__main__":
    print(verify_cancel_all_orders_after_next_month())

