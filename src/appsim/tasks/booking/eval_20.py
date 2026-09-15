from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
ORDER_TYPE_ATTRACTION = "ATTRACTION"
LONDON_GREEN_SKIP_LINE_TICKET_ID = "tkt032"
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    import os
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


def verify_book_london_green_skip_line_ticket_tomorrow(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify that a London Green skip-line ticket (tkt032) has been booked
    for tomorrow with ACTIVE status.

    Task ID: 20
    Logic: Check if any ACTIVE ATTRACTION orders for LONDON_GREEN_SKIP_LINE_TICKET_ID
           have a startDate matching tomorrow's date.
    """
    task_id = 20
    tomorrow = _tomorrow_local_date()

    matching_orders = [
        order
        for order in _orders(task_id, device_id, backup_dir)
        if str(order.get("orderType", "")) == ORDER_TYPE_ATTRACTION
        and str(order.get("itemId", "")) == LONDON_GREEN_SKIP_LINE_TICKET_ID
        and str(order.get("status", "")) == "ACTIVE"
    ]

    return any(_matches_local_date(order.get("startDate"), tomorrow) for order in matching_orders)


if __name__ == "__main__":
    print(verify_book_london_green_skip_line_ticket_tomorrow())
