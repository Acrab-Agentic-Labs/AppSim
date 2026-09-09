from __future__ import annotations

import os

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME = "runtime_account_action_signals.json"
ACTION_SPEND_CALCULATED = "SPEND_CALCULATED"
BASELINE_SPENT_AMOUNT = 4435.0

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


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _account_action_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    for item in reversed(records):
        if predicate(item):
            return item
    return None


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


def _float_value(value, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return default


def _float_close(actual: float, expected: float, tolerance: float = 0.01) -> bool:
    return abs(actual - expected) <= tolerance


def _result_contains_number(result, expected_number: int | float) -> bool:
    import re

    text = _extract_result_broad_text(result)
    if not text:
        return False
    normalized = _normalize_text(text).replace(",", "")
    token = str(int(expected_number)) if isinstance(expected_number, float) and expected_number.is_integer() else str(expected_number).rstrip("0").rstrip(".")
    pattern = rf"(?<!\d){re.escape(token)}(?:\.0+)?(?!\d)"
    return re.search(pattern, normalized) is not None


RESULT_SKIP_KEYS = {"point", "path", "screenshot_path", "image"}


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
    import re

    lowered = text.replace("-", " ").replace("_", " ").lower()
    return re.sub(r"\s+", " ", lowered).strip()


TASK23_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the total amount spent.",
    "properties": {
        "amount": {
            "type": "number",
            "description": "The total amount spent in USD.",
        }
    },
    "required": ["amount"],
    "additionalProperties": False,
}


def verify_calculate_spent_amount(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Task 24: Verify total spent amount calculation.

    Checks:
    - SPEND_CALCULATED action exists with correct amount
    - Result contains the baseline spent amount
    """
    task_id = 24

    spend_action = _latest_account_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_SPEND_CALCULATED
    )
    amount = _float_value(_as_dict(spend_action).get("amount")) if spend_action else 0.0
    state_ok = bool(spend_action and _float_close(amount, BASELINE_SPENT_AMOUNT))

    if isinstance(result, dict) and isinstance(result.get("extracted_answer"), dict):
        ea_amount = _float_value(result["extracted_answer"].get("amount"))
        answer_ok = ea_amount is not None and _float_close(ea_amount, BASELINE_SPENT_AMOUNT)
    else:
        answer_ok = _result_contains_number(result, BASELINE_SPENT_AMOUNT)

    return state_ok and answer_ok


if __name__ == "__main__":
    print(verify_calculate_spent_amount())

