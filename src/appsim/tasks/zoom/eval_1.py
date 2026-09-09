from __future__ import annotations

import json
import logging
import os
import pathlib
from functools import lru_cache

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"

ACTION_INVITE_CONTACTS = "INVITE_CONTACTS"
ACTION_COPY_INVITE_LINK = "COPY_INVITE_LINK"
ACTION_COPY_MEETING_NUMBER = "COPY_MEETING_NUMBER"
ACTION_MEETING_EXITED = "MEETING_EXITED"

FIXTURES_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "zoom", f"task_{task_id:02d}")


def _load_fixture_json(filename: str):
    """Load fixture JSON file."""
    with (FIXTURES_DIR / filename).open("r", encoding="utf-8") as handle:
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
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, "runtime_instant_meetings.json", device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _meeting_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all meeting actions."""
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, "runtime_meeting_actions.json", device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching the predicate."""
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _matching_instant_sessions(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    source: str | None = None,
    meeting_number: str | None = None,
    use_personal_meeting_id: bool | None = None,
) -> list[dict]:
    """Find instant sessions matching criteria."""
    sessions = _instant_meetings(task_id, device_id, backup_dir)

    def predicate(session: dict) -> bool:
        if source and str(session.get("source", "")) != source:
            return False
        if meeting_number and str(session.get("meetingNumber", "")) != str(meeting_number):
            return False
        if use_personal_meeting_id is not None and bool(session.get("usePersonalMeetingId")) != use_personal_meeting_id:
            return False
        return True

    return [session for session in sessions if predicate(session)]


def _find_instant_session(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    source: str | None = None,
    meeting_number: str | None = None,
    use_personal_meeting_id: bool | None = None,
) -> dict | None:
    """Find the latest instant session matching criteria."""
    matches = _matching_instant_sessions(
        task_id,
        device_id,
        backup_dir,
        source=source,
        meeting_number=meeting_number,
        use_personal_meeting_id=use_personal_meeting_id,
    )
    return matches[-1] if matches else None


def _normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    import re
    return re.sub(r"\s+", " ", text).strip().lower()


def _find_meeting_action(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    action_type: str,
    meeting_id: str | None = None,
    meeting_number: str | None = None,
    required_target_ids: list[str] | None = None,
    emoji: str | None = None,
    note_keywords: list[str] | None = None,
    screen_sharing_enabled: bool | None = None,
    microphone_on: bool | None = None,
    camera_on: bool | None = None,
    audio_option: str | None = None,
    exit_action: str | None = None,
    media_change_source: str | None = None,
) -> dict | None:
    """Find a meeting action matching criteria."""
    import re

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
        if emoji is not None and str(action.get("emoji", "")) != emoji:
            return False
        if screen_sharing_enabled is not None and action.get("screenSharingEnabled") != screen_sharing_enabled:
            return False
        if microphone_on is not None and action.get("microphoneOn") != microphone_on:
            return False
        if camera_on is not None and action.get("cameraOn") != camera_on:
            return False
        if audio_option is not None and str(action.get("audioOption", "")) != audio_option:
            return False
        if exit_action is not None and str(action.get("exitAction", "")) != exit_action:
            return False
        if media_change_source is not None and str(action.get("mediaChangeSource", "")) != media_change_source:
            return False
        if note_keywords:
            note_text = str(action.get("note", ""))
            normalized = _normalize_text(note_text)
            if not all(_normalize_text(keyword) in normalized for keyword in note_keywords):
                return False
        return True

    return _find_latest(actions, predicate)


def verify_invite_amber_to_new_meeting(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Task 2: Verify that the user:
    1. Started a HOST instant meeting (non-PMI)
    2. Meeting topic contains "[GUIA-02] Instant Sync"
    3. Waiting room enabled
    4. Allow join before host is disabled (False)
    5. Invited Amber Campbell and Brittany Evans
    6. Copied the meeting number
    7. Copied the invite link
    8. Ended the meeting with END_FOR_ALL
    """
    task_id = 2

    amber_id = _find_user_id("Amber Campbell")
    brittany_id = _find_user_id("Brittany Evans")
    required_invitees = {amber_id, brittany_id} - {""}

    # Find HOST instant session without PMI
    host_session = _find_instant_session(
        task_id,
        device_id,
        backup_dir,
        source="HOST",
        use_personal_meeting_id=False,
    )
    meeting_id = str(host_session.get("signalId", "")) if host_session else ""

    # Check all conditions
    passed = bool(
        host_session
        and _normalize_text("[GUIA-02] Instant Sync") in _normalize_text(str(host_session.get("topic", "")))
        and bool(host_session.get("waitingRoomEnabled"))
        and bool(host_session.get("allowJoinBeforeHost")) is False
        and _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_INVITE_CONTACTS,
            meeting_id=meeting_id,
            required_target_ids=list(required_invitees),
        )
        and _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_COPY_MEETING_NUMBER,
            meeting_id=meeting_id,
        )
        and _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_COPY_INVITE_LINK,
            meeting_id=meeting_id,
        )
        and _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_MEETING_EXITED,
            meeting_id=meeting_id,
            exit_action="END_FOR_ALL",
        )
    )

    return passed


if __name__ == "__main__":
    print(verify_invite_amber_to_new_meeting())
