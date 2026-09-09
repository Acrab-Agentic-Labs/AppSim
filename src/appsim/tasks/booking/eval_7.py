"""
Evaluation logic for Booking task 7: Book cheapest Wuhan to London flight
"""
from __future__ import annotations

import os

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_FLIGHT = "FLIGHT"
CHEAPEST_WUH_TO_LHR_FLIGHT_ID = "flt021"

_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path for a given task."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "booking", f"task_{task_id:02d}")


def _read_runtime_json(
    task_id: int, filename: str, device_id: str | None, backup_dir: str | None
):
    """Read a runtime JSON file from device or backup."""
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
    """Safely convert a value to a list."""
    return value if isinstance(value, list) else []


def _orders(
    task_id: int, device_id: str | None, backup_dir: str | None
) -> list[dict]:
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


def verify_book_cheapest_wuhan_to_london_flight(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify that the cheapest Wuhan to London flight has been booked.

    Task 7: Book the cheapest flight from Wuhan (WUH) to London (LHR)

    Success criteria:
    - An ACTIVE order exists for flight item ID 'flt021'
    - The order type is FLIGHT
    """
    task_id = 7

    # Find the latest order for the cheapest Wuhan to London flight
    order = _latest_order_by_items(
        task_id,
        device_id,
        backup_dir,
        order_type=ORDER_TYPE_FLIGHT,
        item_ids={CHEAPEST_WUH_TO_LHR_FLIGHT_ID},
        status="ACTIVE",
    )

    # Verify that an order exists
    return bool(order)


if __name__ == "__main__":
    print(verify_book_cheapest_wuhan_to_london_flight())

