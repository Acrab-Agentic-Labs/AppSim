from __future__ import annotations

import logging
import os
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
RUNTIME_SCHEDULED_MEETINGS_FILE = "runtime_scheduled_meetings.json"
RUNTIME_DIRECT_MESSAGES_FILE = "runtime_direct_messages.json"
RUNTIME_MEETING_ACTIONS_FILE = "runtime_meeting_actions.json"
SHANGHAI_TZ = timezone(timedelta(hours=8))
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}

# Keyword groups for message matching
UPDATED_LINK_MESSAGE_KEYWORD_GROUPS = [['meeting link', 'updated', 'check'], ['meeting link', 'updated', 'please check']]

# Action types
ACTION_COPY_INVITE_LINK = "COPY_INVITE_LINK"


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


def _scheduled_meetings(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_SCHEDULED_MEETINGS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _direct_messages(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_DIRECT_MESSAGES_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _meeting_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_MEETING_ACTIONS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _is_seed_meeting(signal: dict, index: int) -> bool:
    return str(signal.get("signalId", "")).endswith(f"seed_{index}")


def _find_seed_meeting(task_id: int, device_id: str | None, backup_dir: str | None, index: int) -> dict | None:
    return _find_latest(_scheduled_meetings(task_id, device_id, backup_dir), lambda signal: _is_seed_meeting(signal, index))


def _find_user_id(name: str) -> str:
    """Helper to find user ID from fixtures. Simplified for eval_10.py."""
    # This is a simplified version - in production, this would load from fixtures
    user_map = {
        "Derek Stewart": "user003",
        "Brittany Evans": "user004",
    }
    return user_map.get(name, "")


def _normalize_text(text: str) -> str:
    import re
    return re.sub(r"\s+", " ", text).strip().lower()


def _text_matches_groups(text: str, groups: list[list[str]]) -> bool:
    normalized = _normalize_text(text)
    return any(all(_normalize_text(keyword) in normalized for keyword in group) for group in groups)


def _find_meeting_action(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    action_type: str,
    meeting_id: str | None = None,
) -> dict | None:
    actions = _meeting_actions(task_id, device_id, backup_dir)

    def predicate(action: dict) -> bool:
        if str(action.get("actionType", "")) != action_type:
            return False
        if meeting_id and str(action.get("meetingId", "")) != str(meeting_id):
            return False
        return True

    return _find_latest(actions, predicate)


def _direct_message_exists(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    partner_user_id: str,
    keyword_groups: list[list[str]] | None = None,
    require_link: bool = False,
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
        if require_link and "https://zoom.us/j/" not in content.lower():
            continue
        return True
    return False


def verify_unmute_all_389257198(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 11: Copy the morning meeting invite link and send to Derek and Brittany.

    Expected behavior:
    - The morning meeting (seed index 1) invite link should be copied
    - Direct messages sent to Derek Stewart with updated link keywords and the link
    - Direct messages sent to Brittany Evans with updated link keywords and the link
    """
    task_id = 11

    # Find user IDs
    derek_id = _find_user_id("Derek Stewart")
    brittany_id = _find_user_id("Brittany Evans")

    # Find the morning meeting (seed index 1)
    morning_meeting = _find_seed_meeting(task_id, device_id, backup_dir, 1)
    meeting_id = str(morning_meeting.get("signalId", "")) if morning_meeting else ""

    # Verify all requirements
    return bool(
        morning_meeting
        and _find_meeting_action(task_id, device_id, backup_dir, action_type=ACTION_COPY_INVITE_LINK, meeting_id=meeting_id)
        and derek_id
        and _direct_message_exists(
            task_id,
            device_id,
            backup_dir,
            partner_user_id=derek_id,
            keyword_groups=UPDATED_LINK_MESSAGE_KEYWORD_GROUPS,
            require_link=True,
        )
        and brittany_id
        and _direct_message_exists(
            task_id,
            device_id,
            backup_dir,
            partner_user_id=brittany_id,
            keyword_groups=UPDATED_LINK_MESSAGE_KEYWORD_GROUPS,
            require_link=True,
        )
    )


if __name__ == "__main__":
    print(verify_unmute_all_389257198())

