from __future__ import annotations

import os
import re
from datetime import timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
PRIMARY_USER_ID = "user001"
RUNTIME_USERS_FILE_NAME = "runtime_users.json"
RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME = "runtime_account_action_signals.json"
ACTION_PROFILE_UPDATED = "PROFILE_UPDATED"
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


def _runtime_users(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_USERS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _account_action_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    payload = _read_runtime_json(task_id, RUNTIME_ACCOUNT_ACTION_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _current_user(task_id: int, device_id: str | None, backup_dir: str | None) -> dict:
    return _find_latest(_runtime_users(task_id, device_id, backup_dir), lambda user: str(user.get("userId", "")) == PRIMARY_USER_ID) or {}


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


def verify_update_profile_first_name_to_peter(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Task 22: Verify profile name was updated to 'Peter Liu'.

    Checks:
    - User firstName is 'Peter'
    - User lastName is 'Liu'
    - Profile update action for 'name' field exists
    - Fallback: result text contains 'peter' and 'liu'
    """
    task_id = 22

    user = _current_user(task_id, device_id, backup_dir)
    profile_action = _latest_account_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_PROFILE_UPDATED,
        field_name="name",
    )
    json_ok = bool(
        user
        and str(user.get("firstName", "")) == "Peter"
        and str(user.get("lastName", "")) == "Liu"
        and profile_action
    )
    fallback_ok = _result_contains_any_group(
        result,
        [["peter", "liu"]],
        broad=True
    )
    return json_ok or fallback_ok


if __name__ == "__main__":
    print(verify_update_profile_first_name_to_peter())

