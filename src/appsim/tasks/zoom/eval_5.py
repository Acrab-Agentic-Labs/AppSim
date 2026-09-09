from __future__ import annotations

import logging
import os
import re
from datetime import datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"
RUNTIME_SCHEDULED_MEETINGS_FILE = "runtime_scheduled_meetings.json"
RUNTIME_INSTANT_MEETINGS_FILE = "runtime_instant_meetings.json"
RUNTIME_CHAT_MESSAGES_FILE = "runtime_chat_messages.json"
RUNTIME_MEETING_ACTIONS_FILE = "runtime_meeting_actions.json"
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Action types
ACTION_MEETING_EXITED = "MEETING_EXITED"

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


def _as_dict(value) -> dict:
    return value if isinstance(value, dict) else {}


def _instant_meetings(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_INSTANT_MEETINGS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _chat_messages(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_CHAT_MESSAGES_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _meeting_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_MEETING_ACTIONS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
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
    use_personal_meeting_id: bool | None = None
) -> list[dict]:
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
    use_personal_meeting_id: bool | None = None
) -> dict | None:
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
    return re.sub(r"\s+", " ", text).strip().lower()


def _text_contains_all(text: str, keywords: list[str]) -> bool:
    normalized = _normalize_text(text)
    return all(_normalize_text(keyword) in normalized for keyword in keywords)


def _text_matches_groups(text: str, groups: list[list[str]]) -> bool:
    normalized = _normalize_text(text)
    return any(all(_normalize_text(keyword) in normalized for keyword in group) for group in groups)


def _chat_message_exists(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    meeting_ids: set[str] | None = None,
    content_exact: str | None = None,
    keyword_groups: list[list[str]] | None = None
) -> bool:
    normalized_exact = _normalize_text(content_exact) if content_exact is not None else None
    for message in reversed(_chat_messages(task_id, device_id, backup_dir)):
        if str(message.get("senderId", "")) != CURRENT_USER_ID:
            continue
        if meeting_ids and str(message.get("meetingId", "")) not in meeting_ids:
            continue
        content = str(message.get("content", ""))
        if normalized_exact is not None and _normalize_text(content) != normalized_exact:
            continue
        if keyword_groups and not _text_matches_groups(content, keyword_groups):
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
    emoji: str | None = None,
    note_keywords: list[str] | None = None,
    screen_sharing_enabled: bool | None = None,
    microphone_on: bool | None = None,
    camera_on: bool | None = None,
    audio_option: str | None = None,
    exit_action: str | None = None,
    media_change_source: str | None = None
) -> dict | None:
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
        if note_keywords and not _text_contains_all(str(action.get("note", "")), note_keywords):
            return False
        return True

    return _find_latest(actions, predicate)


def _actions_for_meeting(task_id: int, device_id: str | None, backup_dir: str | None, meeting_id: str) -> list[dict]:
    if not meeting_id:
        return []
    return [
        action
        for action in _meeting_actions(task_id, device_id, backup_dir)
        if str(action.get("meetingId", "")) == meeting_id
    ]


def _resolve_effective_media_state(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    meeting_id: str,
) -> dict | None:
    if not meeting_id:
        return None
    ACTION_MEETING_MEDIA_STATE_CHANGED = "MEETING_MEDIA_STATE_CHANGED"
    ACTION_MEETING_STARTED = "MEETING_STARTED"
    latest_media_change = _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_MEETING_MEDIA_STATE_CHANGED,
        meeting_id=meeting_id,
    )
    if latest_media_change is not None:
        return latest_media_change
    return _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_MEETING_STARTED,
        meeting_id=meeting_id,
    )


def _media_state_matches(
    media_state: dict | None,
    *,
    microphone_on: bool | None = None,
    camera_on: bool | None = None,
    audio_option: str | None = None,
    media_change_source: str | None = None,
) -> bool:
    if not isinstance(media_state, dict):
        return False
    if microphone_on is not None and media_state.get("microphoneOn") != microphone_on:
        return False
    if camera_on is not None and media_state.get("cameraOn") != camera_on:
        return False
    if audio_option is not None and str(media_state.get("audioOption", "")) != audio_option:
        return False
    if media_change_source is not None and str(media_state.get("mediaChangeSource", "")) != media_change_source:
        return False
    return True


def verify_media_enabled_before_host(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify that the user:
    1. Hosted an instant meeting
    2. Started with microphone on, camera on, and no audio connection
    3. Sent a chat message "Audio disconnected, video on."
    4. Ended the meeting for all
    """
    task_id = 6

    # Find the host session
    host_session = _find_instant_session(
        task_id,
        device_id,
        backup_dir,
        source="HOST",
        use_personal_meeting_id=False
    )
    meeting_id = str(host_session.get("signalId", "")) if host_session else ""

    # Check media state (microphone on, camera on, audio_option="none")
    media_state = _resolve_effective_media_state(
        task_id,
        device_id,
        backup_dir,
        meeting_id
    )
    has_correct_media_state = _media_state_matches(
        media_state,
        microphone_on=True,
        camera_on=True,
        audio_option="none"
    )

    # Check if the chat message was sent
    has_chat = _chat_message_exists(
        task_id,
        device_id,
        backup_dir,
        meeting_ids={meeting_id},
        content_exact="Audio disconnected, video on.",
    )

    # Check if the meeting was ended for all
    has_end_for_all = _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_MEETING_EXITED,
        meeting_id=meeting_id,
        exit_action="END_FOR_ALL",
    ) is not None

    # Determine if all criteria are met
    passed = bool(
        host_session
        and has_correct_media_state
        and has_chat
        and has_end_for_all
    )

    return passed


if __name__ == "__main__":
    print(verify_media_enabled_before_host())

