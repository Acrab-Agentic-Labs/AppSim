from __future__ import annotations

import logging
import os
import re
from datetime import datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants from _shared.py
PACKAGE_NAME = "com.example.zoom"
RUNTIME_DIRECT_MESSAGES_FILE = "runtime_direct_messages.json"
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Keyword groups from _shared.py
LEAVE_MESSAGE_KEYWORD_GROUPS = [
    ['next monday', 'leave'],
    ['next monday', 'miss'],
    ['next monday', 'meeting', 'leave'],
    ['take leave', 'next monday']
]

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "zoom", f"task_{task_id:02d}")


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


def _direct_messages(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, RUNTIME_DIRECT_MESSAGES_FILE, device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _text_contains_all(text: str, keywords: list[str]) -> bool:
    normalized = _normalize_text(text)
    return all(_normalize_text(keyword) in normalized for keyword in keywords)


def _text_matches_groups(text: str, groups: list[list[str]]) -> bool:
    normalized = _normalize_text(text)
    return any(all(_normalize_text(keyword) in normalized for keyword in group) for group in groups)


def _find_user_id(name: str) -> str:
    """Simplified user lookup - imports from fixtures if available."""
    import json
    import pathlib

    fixtures_dir = pathlib.Path(__file__).resolve().parent / "fixtures"
    try:
        with (fixtures_dir / "users.json").open("r", encoding="utf-8") as f:
            users = json.load(f)
        for user in users:
            if isinstance(user, dict) and user.get("username") == name:
                return str(user.get("userId", ""))
    except Exception:
        pass
    return ""


def _direct_message_exists(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    partner_user_id: str,
    keyword_groups: list[list[str]] | None = None,
) -> bool:
    CURRENT_USER_ID = "user001"
    for message in reversed(_direct_messages(task_id, device_id, backup_dir)):
        if str(message.get("senderId", "")) != CURRENT_USER_ID:
            continue
        if str(message.get("partnerUserId", "")) != str(partner_user_id):
            continue
        content = str(message.get("content", ""))
        if keyword_groups and not _text_matches_groups(content, keyword_groups):
            continue
        return True
    return False


def verify_upcoming_schedule_count_answer(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    task_id = 14
    natalie_id = _find_user_id("Natalie Cox")
    return bool(
        natalie_id
        and _direct_message_exists(
            task_id,
            device_id,
            backup_dir,
            partner_user_id=natalie_id,
            keyword_groups=LEAVE_MESSAGE_KEYWORD_GROUPS,
        )
    )


if __name__ == "__main__":
    print(verify_upcoming_schedule_count_answer())

