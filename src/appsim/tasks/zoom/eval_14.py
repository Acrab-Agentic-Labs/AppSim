"""Evaluation module for Zoom task 15: Check unread count and send confirmation messages."""

from __future__ import annotations

import json
import logging
import os
import pathlib
import re
from functools import lru_cache

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"
RUNTIME_CHAT_THREAD_STATES_FILE = "runtime_chat_thread_states.json"
RUNTIME_DIRECT_MESSAGES_FILE = "runtime_direct_messages.json"
FIXTURES_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "zoom", f"task_{task_id:02d}")


def _load_fixture_json(filename: str):
    with (FIXTURES_DIR / filename).open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _fixture_context() -> dict:
    users = _load_fixture_json("users.json")
    users_by_id = {
        str(user.get("userId")): user
        for user in users
        if isinstance(user, dict) and user.get("userId")
    }
    users_by_name = {
        str(user.get("username")): user
        for user in users
        if isinstance(user, dict) and user.get("username")
    }
    contact_ids = {user_id for user_id in users_by_id if user_id != CURRENT_USER_ID}
    return {
        "users": users,
        "users_by_id": users_by_id,
        "users_by_name": users_by_name,
        "contact_ids": contact_ids,
    }


def _find_user_id(name: str) -> str:
    user = _fixture_context()["users_by_name"].get(name, {})
    return str(user.get("userId", ""))


def _read_runtime_json(task_id: int, filename: str, device_id: str | None, backup_dir: str | None):
    cache_key = (task_id, filename, device_id, backup_dir)
    if cache_key not in _RUNTIME_CACHE:
        resolved_backup_dir = _build_backup_dir(task_id, backup_dir)
        _RUNTIME_CACHE[cache_key] = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{filename}",
            backup_dir=resolved_backup_dir,
        )
    return _RUNTIME_CACHE[cache_key]


def _as_list(value) -> list:
    return value if isinstance(value, list) else []


def _chat_thread_states(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, RUNTIME_CHAT_THREAD_STATES_FILE, device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _direct_messages(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_DIRECT_MESSAGES_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _direct_message_exists(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    partner_user_id: str,
    content_exact: str | None = None,
) -> bool:
    normalized_exact = _normalize_text(content_exact) if content_exact is not None else None
    for message in reversed(_direct_messages(task_id, device_id, backup_dir)):
        if str(message.get("senderId", "")) != CURRENT_USER_ID:
            continue
        if str(message.get("partnerUserId", "")) != str(partner_user_id):
            continue
        content = str(message.get("content", ""))
        if normalized_exact is not None and _normalize_text(content) != normalized_exact:
            continue
        return True
    return False


TASK14_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of unread chat threads after completing the messaging actions.",
    "properties": {
        "unread_count": {
            "type": "integer",
            "minimum": 0,
            "description": "The current number of unread chat threads, returned as an Arabic numeral integer.",
        }
    },
    "required": ["unread_count"],
    "additionalProperties": False,
}

def verify_schedule_tomorrow_1900_with_derek_and_brittany(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 15: Check unread message count and send confirmation messages.

    Task requirements:
    - Extract the correct unread_count from chat thread states
    - Send "Please confirm tomorrow's meeting." to Amber Campbell
    - Send "Please confirm tomorrow's meeting." to Derek Stewart

    Args:
        result: Task execution result with extracted_answer containing unread_count
        device_id: Device identifier for data retrieval
        backup_dir: Backup directory path for offline data
        **kwargs: Additional context (unused)

    Returns:
        True if unread_count matches and both confirmation messages were sent
    """
    task_id = 15
    amber_id = _find_user_id("Amber Campbell")
    derek_id = _find_user_id("Derek Stewart")

    expected_unread = len(
        [
            item
            for item in _chat_thread_states(task_id, device_id, backup_dir)
            if int(item.get("unreadCount", 0)) > 0
        ]
    )
    extracted_answer = result.get("extracted_answer") if isinstance(result, dict) else None
    if not isinstance(extracted_answer, dict) or extracted_answer.get("unread_count") != expected_unread:
        logging.info(
            "Zoom task 15 verify detail: extracted_answer=%r expected_number=%s",
            extracted_answer,
            expected_unread,
        )
        return False
    return bool(
        amber_id
        and _direct_message_exists(
            task_id,
            device_id,
            backup_dir,
            partner_user_id=amber_id,
            content_exact="Please confirm tomorrow's meeting.",
        )
        and derek_id
        and _direct_message_exists(
            task_id,
            device_id,
            backup_dir,
            partner_user_id=derek_id,
            content_exact="Please confirm tomorrow's meeting.",
        )
    )


if __name__ == "__main__":
    print(verify_schedule_tomorrow_1900_with_derek_and_brittany())

