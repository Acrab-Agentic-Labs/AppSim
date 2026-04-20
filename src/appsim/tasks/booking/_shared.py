from __future__ import annotations

import logging
import os
import re
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.booking"
PRIMARY_USER_ID = "user001"

ORDERS_FILE_NAME = "orders.json"
RUNTIME_USERS_FILE_NAME = "runtime_users.json"
RUNTIME_SEARCH_SIGNALS_FILE_NAME = "runtime_search_signals.json"
RUNTIME_BOOKING_SIGNALS_FILE_NAME = "runtime_booking_signals.json"
RUNTIME_HOTEL_REVIEW_SIGNALS_FILE_NAME = "runtime_hotel_review_signals.json"
RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME = "runtime_account_action_signals.json"

SEARCH_TYPE_FLIGHT_SUBMITTED = "FLIGHT_SEARCH_SUBMITTED"

ORDER_TYPE_STAY = "STAY"
ORDER_TYPE_FLIGHT = "FLIGHT"
ORDER_TYPE_CAR_RENTAL = "CAR_RENTAL"
ORDER_TYPE_TAXI = "TAXI"
ORDER_TYPE_ATTRACTION = "ATTRACTION"

ACTION_PROFILE_UPDATED = "PROFILE_UPDATED"
ACTION_SPEND_CALCULATED = "SPEND_CALCULATED"
ACTION_FUTURE_ORDERS_CANCELLED = "FUTURE_ORDERS_CANCELLED"
ACTION_STAY_BOOK_AGAIN_PREPARED = "STAY_BOOK_AGAIN_PREPARED"

BASELINE_SPENT_AMOUNT = 4435.0

LONDON_HOTEL_IDS = {"htl001", "htl016", "htl017", "htl018"}
LONDON_AIRPORT_SHUTTLE_HOTEL_IDS = {"htl016", "htl017"}
CHEAPEST_WUH_TO_LHR_FLIGHT_ID = "flt021"
FIRST_CLASS_HKG_TO_LHR_FLIGHT_ID = "flt023"
PREMIUM_ECONOMY_LHR_TO_SYD_FLIGHT_ID = "flt025"
LHR_CAR_ID = "car004"
HKG_CAR_IDS = {"car013", "car014", "car015", "car016"}
CHEAPEST_HKG_COMFORT_SEDAN_ID = "car015"
LHR_TO_HILTON_TAXI_ROUTE_IDS = {"taxi009", "taxi010"}
HKG_TO_REGAL_LUXURY_TAXI_ROUTE_ID = "taxi012"
PARIS_MOST_EXPENSIVE_VIP_TICKET_ID = "tkt003"
SAGRADA_STANDARD_TICKET_ID = "tkt006"
LONDON_GREEN_SKIP_LINE_TICKET_ID = "tkt032"

TRIP_NAME_ALIAS_KEYWORD_GROUPS = {
    "tokyo skytree observation deck": [
        ["tokyo", "skytree"],
        ["observation", "deck"],
        ["\u4e1c\u4eac", "\u6674\u7a7a\u5854"],
        ["\u6674\u7a7a\u5854", "\u5c55\u671b\u53f0"],
        ["\u4e1c\u4eac", "\u5c55\u671b\u53f0"],
    ],
}


RESULT_SKIP_KEYS = {"point", "path", "screenshot_path", "image"}
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


def _runtime_users(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_USERS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _search_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_SEARCH_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _booking_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_BOOKING_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _hotel_review_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_HOTEL_REVIEW_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _account_action_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _latest_booking(task_id: int, device_id: str | None, backup_dir: str | None, *, order_type: str | None = None, item_ids: set[str] | None = None) -> dict | None:
    allowed_items = {str(item_id) for item_id in (item_ids or set()) if item_id}

    def predicate(signal: dict) -> bool:
        if order_type and str(signal.get("orderType", "")) != order_type:
            return False
        if allowed_items and str(signal.get("itemId", "")) not in allowed_items:
            return False
        return True

    return _find_latest(_booking_signals(task_id, device_id, backup_dir), predicate)


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


def _latest_account_action(task_id: int, device_id: str | None, backup_dir: str | None, *, action_type: str, field_name: str | None = None) -> dict | None:
    def predicate(signal: dict) -> bool:
        if str(signal.get("actionType", "")) != action_type:
            return False
        if field_name is not None:
            extra = _as_dict(signal.get("extra"))
            if str(extra.get("field", "")) != field_name:
                return False
        return True

    return _find_latest(_account_action_signals(task_id, device_id, backup_dir), predicate)


def _future_cancel_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [
        signal
        for signal in _account_action_signals(task_id, device_id, backup_dir)
        if str(signal.get("actionType", "")) == ACTION_FUTURE_ORDERS_CANCELLED
    ]


def _future_cancel_cutoff_millis(action_signal: dict) -> int | None:
    extra = _as_dict(action_signal.get("extra"))
    cutoff_raw = extra.get("cutoffMillis")
    if cutoff_raw is None:
        return None
    try:
        return int(cutoff_raw)
    except Exception:
        return None


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


def _current_user(task_id: int, device_id: str | None, backup_dir: str | None) -> dict:
    return _find_latest(_runtime_users(task_id, device_id, backup_dir), lambda user: str(user.get("userId", "")) == PRIMARY_USER_ID) or {}


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


def _result_contains_number(result, expected_number: int | float) -> bool:
    text = _extract_result_broad_text(result)
    if not text:
        return False
    normalized = _normalize_text(text).replace(",", "")
    token = str(int(expected_number)) if isinstance(expected_number, float) and expected_number.is_integer() else str(expected_number).rstrip("0").rstrip(".")
    pattern = rf"(?<!\d){re.escape(token)}(?:\.0+)?(?!\d)"
    return re.search(pattern, normalized) is not None


def _result_success(result) -> bool:
    return isinstance(result, dict) and bool(result.get("success"))


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
        [f"{start_date.month}\u6708", f"{start_date.day}\u65e5"],
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
        groups.append([f"{rounded_amount}\u7f8e\u5143"])
    return groups


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


def _float_close(actual: float, expected: float, tolerance: float = 0.01) -> bool:
    return abs(actual - expected) <= tolerance


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


def _matches_any_local_date(timestamp_ms, target_dates: set[date]) -> bool:
    actual = _to_local_date(timestamp_ms)
    return actual in target_dates if actual is not None else False


def _matches_local_slot(timestamp_ms, target_date: date, hour: int, minute: int, tolerance_minutes: int = 90) -> bool:
    actual = _to_local_datetime(timestamp_ms)
    if actual is None or actual.date() != target_date:
        return False
    target = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=SHANGHAI_TZ)
    return abs((actual - target).total_seconds()) <= tolerance_minutes * 60


def _today_local_date() -> date:
    return datetime.now(SHANGHAI_TZ).date()


def _tomorrow_local_date() -> date:
    return _today_local_date() + timedelta(days=1)


def _day_after_tomorrow_local_date() -> date:
    return _today_local_date() + timedelta(days=2)


def _next_weekday_candidates(weekday: int) -> set[date]:
    today = _today_local_date()
    delta = (weekday - today.weekday()) % 7
    if delta == 0:
        delta = 7
    return {today + timedelta(days=delta), today + timedelta(days=delta + 7)}


def evaluate_task(task_id: int, result=None, device_id=None, backup_dir=None, **kwargs) -> bool:
    tomorrow = _tomorrow_local_date()
    day_after_tomorrow = _day_after_tomorrow_local_date()
    next_saturday_candidates = _next_weekday_candidates(5)
    next_sunday_candidates = _next_weekday_candidates(6)
    next_monday_candidates = _next_weekday_candidates(0)

    if task_id == 1:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_STAY,
            item_ids=LONDON_HOTEL_IDS,
            status="ACTIVE",
        )
        return bool(order and _int_value(order.get("guestCount")) == 2 and _matches_any_local_date(order.get("startDate"), next_saturday_candidates))

    if task_id == 2:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_STAY,
            item_ids={"htl001"},
            status="ACTIVE",
        )
        return bool(order and _matches_local_date(order.get("startDate"), tomorrow))

    if task_id == 3:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_STAY,
            item_ids={"htl001"},
            status="ACTIVE",
        )
        return bool(order and _matches_local_date(order.get("startDate"), day_after_tomorrow))

    if task_id == 4:
        review = _find_latest(_hotel_review_signals(task_id, device_id, backup_dir), lambda signal: str(signal.get("orderId", "")) == "ord001" and str(signal.get("hotelId", "")) == "htl001")
        json_ok = bool(review and _int_value(review.get("rating")) == 5)
        fallback_ok = _result_contains_any_group(result, [["five", "star", "review"], ["5", "star", "review"]], broad=True)
        return json_ok or fallback_ok

    if task_id == 5:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_STAY,
            item_ids=LONDON_AIRPORT_SHUTTLE_HOTEL_IDS,
            status="ACTIVE",
        )
        return bool(order and _matches_local_date(order.get("startDate"), day_after_tomorrow))

    if task_id == 6:
        prepared = _latest_account_action(task_id, device_id, backup_dir, action_type=ACTION_STAY_BOOK_AGAIN_PREPARED)
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_STAY,
            item_ids={"htl001"},
            status="ACTIVE",
        )
        return bool(prepared and order and _matches_local_date(order.get("startDate"), tomorrow))

    if task_id == 7:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_FLIGHT,
            item_ids={CHEAPEST_WUH_TO_LHR_FLIGHT_ID},
            status="ACTIVE",
        )
        return bool(order)

    if task_id == 8:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_FLIGHT,
            item_ids={FIRST_CLASS_HKG_TO_LHR_FLIGHT_ID},
            status="ACTIVE",
        )
        return bool(order)

    if task_id == 9:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_FLIGHT,
            item_ids={PREMIUM_ECONOMY_LHR_TO_SYD_FLIGHT_ID},
            status="ACTIVE",
        )
        return bool(order)

    if task_id == 10:
        search = _latest_search(task_id, device_id, backup_dir, search_type=SEARCH_TYPE_FLIGHT_SUBMITTED, destination_tokens=("lhr", "hkg"))
        has_flight_booking = _latest_booking(task_id, device_id, backup_dir, order_type=ORDER_TYPE_FLIGHT) is not None
        json_ok = bool(search and _matches_any_local_date(search.get("checkInDate"), next_sunday_candidates) and not has_flight_booking)
        fallback_ok = _result_contains_any_group(result, [["london", "hong", "kong"], ["not", "sure"]], broad=True)
        return json_ok or fallback_ok

    if task_id == 11:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_CAR_RENTAL,
            item_ids={LHR_CAR_ID},
            status="ACTIVE",
        )
        return bool(order and _matches_local_date(order.get("startDate"), day_after_tomorrow) and _matches_local_slot(order.get("startDate"), day_after_tomorrow, 12, 0))

    if task_id == 12:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_CAR_RENTAL,
            item_ids={LHR_CAR_ID},
            status="ACTIVE",
        )
        return bool(order and _matches_any_local_date(order.get("endDate"), next_monday_candidates))

    if task_id == 13:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_CAR_RENTAL,
            item_ids=HKG_CAR_IDS,
            status="ACTIVE",
        )
        item_name = str(order.get("itemName", "")) if order else ""
        return bool(order and _matches_local_date(order.get("startDate"), day_after_tomorrow) and _matches_local_slot(order.get("startDate"), day_after_tomorrow, 12, 0) and "child seat" in item_name.lower())

    if task_id == 14:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_CAR_RENTAL,
            item_ids={CHEAPEST_HKG_COMFORT_SEDAN_ID},
            status="ACTIVE",
        )
        return bool(order and _matches_local_date(order.get("startDate"), day_after_tomorrow) and _matches_local_slot(order.get("startDate"), day_after_tomorrow, 12, 0))

    if task_id == 15:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_TAXI,
            item_ids=LHR_TO_HILTON_TAXI_ROUTE_IDS,
            status="ACTIVE",
        )
        return bool(order and _matches_local_date(order.get("startDate"), _today_local_date()))

    if task_id == 16:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_TAXI,
            item_ids=LHR_TO_HILTON_TAXI_ROUTE_IDS,
            status="ACTIVE",
        )
        return bool(order and _matches_local_slot(order.get("startDate"), tomorrow, 12, 0) and _matches_local_slot(order.get("endDate"), day_after_tomorrow, 8, 0))

    if task_id == 17:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_TAXI,
            item_ids={HKG_TO_REGAL_LUXURY_TAXI_ROUTE_ID},
            status="ACTIVE",
        )
        return bool(order)

    if task_id == 18:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_ATTRACTION,
            item_ids={PARIS_MOST_EXPENSIVE_VIP_TICKET_ID},
            status="ACTIVE",
        )
        return bool(order and _matches_local_date(order.get("startDate"), day_after_tomorrow))

    if task_id == 19:
        order = _latest_order_by_items(
            task_id,
            device_id,
            backup_dir,
            order_type=ORDER_TYPE_ATTRACTION,
            item_ids={SAGRADA_STANDARD_TICKET_ID},
            status="ACTIVE",
        )
        return bool(order)

    if task_id == 20:
        matching_orders = [
            order
            for order in _orders(task_id, device_id, backup_dir)
            if str(order.get("orderType", "")) == ORDER_TYPE_ATTRACTION
            and str(order.get("itemId", "")) == LONDON_GREEN_SKIP_LINE_TICKET_ID
            and str(order.get("status", "")) == "ACTIVE"
        ]
        return any(_matches_local_date(order.get("startDate"), tomorrow) for order in matching_orders)

    if task_id == 21:
        nearest_order = _nearest_upcoming_active_order(task_id, device_id, backup_dir)
        if nearest_order is None:
            return False

        name_groups = _trip_name_keyword_groups(nearest_order)
        date_groups = _trip_date_keyword_groups(nearest_order)
        amount_groups = _trip_amount_keyword_groups(nearest_order)

        has_name = bool(name_groups) and _result_contains_any_group(result, name_groups, broad=True)
        has_date = bool(date_groups) and _result_contains_any_group(result, date_groups, broad=True)
        has_amount = bool(amount_groups) and _result_contains_any_group(result, amount_groups, broad=True)
        return has_name and has_date and has_amount

    if task_id == 22:
        user = _current_user(task_id, device_id, backup_dir)
        profile_action = _latest_account_action(task_id, device_id, backup_dir, action_type=ACTION_PROFILE_UPDATED, field_name="name")
        json_ok = bool(user and str(user.get("firstName", "")) == "Peter" and str(user.get("lastName", "")) == "Liu" and profile_action)
        fallback_ok = _result_contains_any_group(result, [["peter", "liu"]], broad=True)
        return json_ok or fallback_ok

    if task_id == 23:
        user = _current_user(task_id, device_id, backup_dir)
        profile_action = _latest_account_action(task_id, device_id, backup_dir, action_type=ACTION_PROFILE_UPDATED, field_name="phone")
        json_ok = bool(user and "752-0405" in str(user.get("phone", "")) and profile_action)
        fallback_ok = _result_contains_any_group(result, [["752", "0405"]], broad=True)
        return json_ok or fallback_ok

    if task_id == 24:
        spend_action = _latest_account_action(task_id, device_id, backup_dir, action_type=ACTION_SPEND_CALCULATED)
        amount = _float_value(_as_dict(spend_action).get("amount")) if spend_action else 0.0
        return bool(spend_action and _float_close(amount, BASELINE_SPENT_AMOUNT))

    if task_id == 25:
        cancel_actions = _future_cancel_actions(task_id, device_id, backup_dir)
        has_successful_cancel = any(_int_value(action.get("affectedOrderCount")) >= 1 for action in cancel_actions)

        cutoff_candidates = [
            cutoff
            for cutoff in (_future_cancel_cutoff_millis(action) for action in cancel_actions)
            if cutoff is not None
        ]
        latest_cutoff = max(cutoff_candidates) if cutoff_candidates else None
        if latest_cutoff is None:
            return False

        cruise_order = _latest_order(task_id, device_id, backup_dir, item_id="crs001")
        cruise_cancelled = bool(cruise_order and str(cruise_order.get("status", "")) == "CANCELLED")
        no_active_orders_after_cutoff = not _has_active_orders_after_cutoff(
            task_id,
            device_id,
            backup_dir,
            latest_cutoff,
        )
        return has_successful_cancel and cruise_cancelled and no_active_orders_after_cutoff

    logging.error("Unsupported Booking task ID: %s", task_id)
    return False
