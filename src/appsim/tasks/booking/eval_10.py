from __future__ import annotations

import os
import re
from datetime import datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
RUNTIME_SEARCH_SIGNALS_FILE_NAME = "runtime_search_signals.json"
RUNTIME_BOOKING_SIGNALS_FILE_NAME = "runtime_booking_signals.json"
SEARCH_TYPE_FLIGHT_SUBMITTED = "FLIGHT_SEARCH_SUBMITTED"
ORDER_TYPE_FLIGHT = "FLIGHT"
RESULT_SKIP_KEYS = {"point", "path", "screenshot_path", "image"}
SHANGHAI_TZ = timezone(timedelta(hours=8))

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


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _search_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_SEARCH_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _booking_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_BOOKING_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _latest_search(task_id: int, device_id: str | None, backup_dir: str | None, *, search_type: str | None = None, destination_tokens: tuple[str, ...] | None = None) -> dict | None:
    tokens = tuple(token.lower() for token in (destination_tokens or tuple()) if token)

    def predicate(signal: dict) -> bool:
        if search_type and str(signal.get("searchType", "")) != search_type:
            return False
        destination = str(signal.get("destination", "")).lower()
        if tokens and any(token not in destination for token in tokens):
            return False
        return True

    return _find_latest(_search_signals(task_id, device_id, backup_dir), predicate)


def _latest_booking(task_id: int, device_id: str | None, backup_dir: str | None, *, order_type: str | None = None, item_ids: set[str] | None = None) -> dict | None:
    allowed_items = {str(item_id) for item_id in (item_ids or set()) if item_id}

    def predicate(signal: dict) -> bool:
        if order_type and str(signal.get("orderType", "")) != order_type:
            return False
        if allowed_items and str(signal.get("itemId", "")) not in allowed_items:
            return False
        return True

    return _find_latest(_booking_signals(task_id, device_id, backup_dir), predicate)


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


def _normalize_text(text: str) -> str:
    lowered = text.replace("-", " ").replace("_", " ").lower()
    return re.sub(r"\s+", " ", lowered).strip()


def _result_contains_any_group(result, groups: list[list[str]], *, broad: bool = False) -> bool:
    text = _extract_result_broad_text(result) if broad else _extract_result_text(result)
    normalized = _normalize_text(text)
    if not normalized:
        return False
    return any(all(_normalize_text(token) in normalized for token in group) for group in groups)


def _to_local_date(timestamp_ms):
    try:
        dt = datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
        return dt.date()
    except Exception:
        return None


def _matches_any_local_date(timestamp_ms, target_dates: set) -> bool:
    actual = _to_local_date(timestamp_ms)
    return actual in target_dates if actual is not None else False


def _today_local_date():
    return datetime.now(SHANGHAI_TZ).date()


def _next_weekday_candidates(weekday: int):
    today = _today_local_date()
    delta = (weekday - today.weekday()) % 7
    if delta == 0:
        delta = 7
    return {today + timedelta(days=delta), today + timedelta(days=delta + 7)}


def verify_search_london_to_hong_kong_next_sunday_without_booking(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    task_id = 10
    next_sunday_candidates = _next_weekday_candidates(6)  # 6 = Sunday

    search = _latest_search(task_id, device_id, backup_dir, search_type=SEARCH_TYPE_FLIGHT_SUBMITTED, destination_tokens=("lhr", "hkg"))
    has_flight_booking = _latest_booking(task_id, device_id, backup_dir, order_type=ORDER_TYPE_FLIGHT) is not None
    json_ok = bool(search and _matches_any_local_date(search.get("checkInDate"), next_sunday_candidates) and not has_flight_booking)
    fallback_ok = _result_contains_any_group(result, [["london", "hong", "kong"], ["not", "sure"]], broad=True)
    return json_ok or fallback_ok


if __name__ == "__main__":
    print(verify_search_london_to_hong_kong_next_sunday_without_booking())
