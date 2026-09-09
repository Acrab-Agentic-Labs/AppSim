from __future__ import annotations

import json
import logging
import os
from functools import lru_cache

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"
RUNTIME_INSTANT_MEETINGS_FILE = "runtime_instant_meetings.json"
RUNTIME_CHAT_MESSAGES_FILE = "runtime_chat_messages.json"
RUNTIME_MEETING_ACTIONS_FILE = "runtime_meeting_actions.json"

ACTION_MUTE_ALL = "MUTE_ALL"
ACTION_PARTICIPANT_UNMUTE = "PARTICIPANT_UNMUTE"
ACTION_LOCK_MEETING = "LOCK_MEETING"

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "zoom", f"task_{task_id:02d}")


def _load_fixture_json(filename: str):
    """Load fixture JSON file."""
    import pathlib
    fixtures_dir = pathlib.Path(__file__).resolve().parent / "fixtures"
    with (fixtures_dir / filename).open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _fixture_context() -> dict:
    """Load and cache fixture context."""
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
    """Find user ID by username."""
    user = _fixture_context()["users_by_name"].get(name, {})
    return str(user.get("userId", ""))


def _read_runtime_json(task_id: int, filename: str, device_id: str | None, backup_dir: str | None):
    """Read runtime JSON from device or backup."""
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
    """Convert value to list if possible."""
    return value if isinstance(value, list) else []


def _instant_meetings(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all instant meetings."""
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_INSTANT_MEETINGS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _chat_messages(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all chat messages."""
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_CHAT_MESSAGES_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _meeting_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all meeting actions."""
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_MEETING_ACTIONS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    import re
    return re.sub(r"\s+", " ", text).strip().lower()


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching the predicate."""
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _chat_message_exists(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    meeting_ids: set[str] | None = None,
    content_exact: str | None = None,
) -> bool:
    """Check if a chat message exists with exact content."""
    normalized_exact = _normalize_text(content_exact) if content_exact is not None else None
    for message in reversed(_chat_messages(task_id, device_id, backup_dir)):
        if str(message.get("senderId", "")) != CURRENT_USER_ID:
            continue
        if meeting_ids and str(message.get("meetingId", "")) not in meeting_ids:
            continue
        content = str(message.get("content", ""))
        if normalized_exact is not None and _normalize_text(content) != normalized_exact:
            continue
        return True
    return False


def _find_meeting_action(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    action_type: str,
    meeting_id: str | None = None,
    meeting_number: str | None = None,
    required_target_ids: list[str] | None = None,
) -> dict | None:
    """Find a meeting action matching the criteria."""
    required_targets = {str(target_id) for target_id in (required_target_ids or []) if target_id}
    actions = _meeting_actions(task_id, device_id, backup_dir)

    def predicate(action: dict) -> bool:
        if str(action.get("actionType", "")) != action_type:
            return False
        if meeting_id and str(action.get("meetingId", "")) != str(meeting_id):
            return False
        if meeting_number and str(action.get("meetingNumber", "")) != str(meeting_number):
            return False
        target_ids = {str(target_id) for target_id in _as_list(action.get("targetUserIds")) if target_id}
        if required_targets and not required_targets.issubset(target_ids):
            return False
        return True

    return _find_latest(actions, predicate)


def verify_screen_share_in_new_meeting(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Task 4: Mute all participants in meeting 389257198, unmute Amber Campbell,
    send chat message "Amber, please start.", then lock the meeting.
    """
    task_id = 4

    # Find Amber Campbell's user ID
    amber_id = _find_user_id("Amber Campbell")

    # Get all meeting sessions for meeting number 389257198
    target_meeting_ids = {
        str(session.get("signalId"))
        for session in _instant_meetings(task_id, device_id, backup_dir)
        if str(session.get("meetingNumber", "")) == "389257198" and session.get("signalId")
    }

    # Check chat message: "Amber, please start."
    has_chat = _chat_message_exists(
        task_id,
        device_id,
        backup_dir,
        meeting_ids=target_meeting_ids,
        content_exact="Amber, please start.",
    )

    # Check mute all action
    has_mute_all = _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_MUTE_ALL,
        meeting_number="389257198",
    ) is not None

    # Check unmute Amber action
    has_unmute_amber = bool(
        amber_id
        and _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_PARTICIPANT_UNMUTE,
            meeting_number="389257198",
            required_target_ids=[amber_id],
        ) is not None
    )

    # Check lock meeting action
    has_lock_meeting = _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_LOCK_MEETING,
        meeting_number="389257198",
    ) is not None

    # Check if all conditions are met
    passed = bool(
        has_mute_all
        and has_unmute_amber
        and has_chat
        and has_lock_meeting
    )

    # Log detailed debug information if verification failed
    if not passed:
        logging.info(
            "Zoom task 4 verify detail: mute_all=%s unmute_amber=%s chat_exact=%s lock_meeting=%s amber_id=%s",
            has_mute_all,
            has_unmute_amber,
            has_chat,
            has_lock_meeting,
            amber_id,
        )

    return passed


if __name__ == "__main__":
    print(verify_screen_share_in_new_meeting())

