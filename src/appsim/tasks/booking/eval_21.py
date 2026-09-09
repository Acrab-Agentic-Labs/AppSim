from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
ORDERS_FILE_NAME = "orders.json"
SHANGHAI_TZ = timezone(timedelta(hours=8))

TRIP_NAME_ALIAS_KEYWORD_GROUPS = {
    "tokyo skytree observation deck": [
        ["tokyo", "skytree"],
        ["observation", "deck"],
        ["东京", "晴空塔"],
        ["晴空塔", "展望台"],
        ["东京", "展望台"],
    ],
}

RESULT_SKIP_KEYS = {"point", "path", "screenshot_path", "image"}

_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


TASK21_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract information about the nearest upcoming trip.",
    "properties": {
        "trip_name": {
            "type": "string",
            "description": "The name or title of the nearest upcoming trip.",
        },
        "trip_date": {
            "type": "string",
            "description": "The date of the trip.",
        },
        "trip_amount": {
            "type": "string",
            "description": "The cost/amount of the trip.",
        },
    },
    "required": ["trip_name"],
    "additionalProperties": False,
}


# Helper functions
def _as_list(value) -> list:
    return value if isinstance(value, list) else []


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


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
            fallback_dir=_build_backup_dir(task_id, backup_dir),
        )
    return _RUNTIME_CACHE[cache_key]


def _orders(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, ORDERS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _int_value(value, default: int = 0) -> int:
    try:
        return int(value)
    except Exception:
        return default


def _float_value(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _to_local_date(timestamp_ms):
    from datetime import date
    try:
        dt = datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
        return dt.date() if dt is not None else None
    except Exception:
        return None


def _normalize_text(text: str) -> str:
    lowered = text.replace("-", " ").replace("_", " ").lower()
    return re.sub(r"\s+", " ", lowered).strip()


def _append_named_strings(source: dict, keys: tuple[str, ...], chunks: list[str]) -> None:
    for key in keys:
        value = source.get(key)
        if isinstance(value, str):
            text = value.strip()
            if text:
                chunks.append(text)


def _collect_all_strings(value, chunks: list[str]) -> None:
    if isinstance(value, str):
        text = value.strip()
        if text:
            chunks.append(text)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if key in RESULT_SKIP_KEYS:
                continue
            _collect_all_strings(item, chunks)
        return
    if isinstance(value, list):
        for item in value:
            _collect_all_strings(item, chunks)


def _extract_result_text(result) -> str:
    if not isinstance(result, dict):
        return ""
    chunks: list[str] = []
    _append_named_strings(result, ("final_answer", "answer", "content", "message", "final_message", "summary"), chunks)
    for action in _as_list(result.get("executed_actions")):
        if isinstance(action, dict):
            _append_named_strings(action, ("content", "message", "text", "thought", "reason", "observation", "status", "description"), chunks)
    return "\n".join(chunks)


def _extract_result_broad_text(result) -> str:
    if not isinstance(result, dict):
        return ""
    chunks: list[str] = []
    _collect_all_strings(result, chunks)
    return "\n".join(chunks)


def _result_contains_any_group(result, groups: list[list[str]], *, broad: bool = False) -> bool:
    text = _extract_result_broad_text(result) if broad else _extract_result_text(result)
    normalized = _normalize_text(text)
    if not normalized:
        return False
    return any(all(_normalize_text(token) in normalized for token in group) for group in groups)


def _nearest_upcoming_active_order(task_id: int, device_id: str | None, backup_dir: str | None) -> dict | None:
    active_orders = [
        order
        for order in _orders(task_id, device_id, backup_dir)
        if str(order.get("status", "")) == "ACTIVE"
    ]
    if not active_orders:
        return None

    now_ms = int(datetime.now(SHANGHAI_TZ).timestamp() * 1000)
    future_orders = [
        order
        for order in active_orders
        if _int_value(order.get("startDate"), -1) >= now_ms
    ]

    candidate_orders = future_orders if future_orders else active_orders
    return min(candidate_orders, key=lambda order: _int_value(order.get("startDate"), 10**18))


def _trip_name_keyword_groups(order: dict) -> list[list[str]]:
    item_name = str(order.get("itemName", "")).strip()
    if not item_name:
        return []

    normalized_item_name = _normalize_text(item_name)
    keyword_groups = list(TRIP_NAME_ALIAS_KEYWORD_GROUPS.get(normalized_item_name, []))

    token_candidates = [
        token
        for token in re.split(r"\s+", normalized_item_name)
        if token and not token.isdigit()
    ]
    if len(token_candidates) >= 2:
        keyword_groups.append(token_candidates[:2])
    elif token_candidates:
        keyword_groups.append([token_candidates[0]])

    keyword_groups.append([item_name])
    return keyword_groups


def _trip_date_keyword_groups(order: dict) -> list[list[str]]:
    start_date = _to_local_date(order.get("startDate"))
    if start_date is None:
        return []

    iso_date = f"{start_date.year}-{start_date.month:02d}-{start_date.day:02d}"
    slash_date = f"{start_date.month}/{start_date.day}"
    return [
        [str(start_date.year), str(start_date.month), str(start_date.day)],
        [iso_date],
        [slash_date],
        [f"{start_date.month}月", f"{start_date.day}日"],
    ]


def _trip_amount_keyword_groups(order: dict) -> list[list[str]]:
    amount = _float_value(order.get("totalPrice"))
    if amount <= 0:
        return []

    rounded_amount = int(round(amount))
    groups = [[str(rounded_amount)], [f"${rounded_amount}"]]
    currency = str(order.get("currency", "")).upper()
    if currency:
        groups.append([str(rounded_amount), currency.lower()])
    if currency == "USD":
        groups.append([f"{rounded_amount}美元"])
    return groups


# Main verification function
def verify_answer_nearest_upcoming_trip(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 21: Extract information about the nearest upcoming trip.

    This function checks if the result contains:
    1. The name/title of the nearest upcoming trip
    2. The date of the trip
    3. The cost/amount of the trip
    """
    task_id = 21

    nearest_order = _nearest_upcoming_active_order(task_id, device_id, backup_dir)
    if nearest_order is None:
        return False

    name_groups = _trip_name_keyword_groups(nearest_order)
    date_groups = _trip_date_keyword_groups(nearest_order)
    amount_groups = _trip_amount_keyword_groups(nearest_order)

    if isinstance(result, dict) and isinstance(result.get("extracted_answer"), dict):
        ea = result["extracted_answer"]
        ea_text = " ".join(str(v) for v in ea.values() if v)
        norm = _normalize_text(ea_text)
        has_name = bool(name_groups) and any(all(_normalize_text(t) in norm for t in g) for g in name_groups)
        has_date = bool(date_groups) and any(all(_normalize_text(t) in norm for t in g) for g in date_groups)
        has_amount = bool(amount_groups) and any(all(_normalize_text(t) in norm for t in g) for g in amount_groups)
    else:
        has_name = bool(name_groups) and _result_contains_any_group(result, name_groups, broad=True)
        has_date = bool(date_groups) and _result_contains_any_group(result, date_groups, broad=True)
        has_amount = bool(amount_groups) and _result_contains_any_group(result, amount_groups, broad=True)
    return has_name and has_date and has_amount


if __name__ == "__main__":
    print(verify_answer_nearest_upcoming_trip())



