from __future__ import annotations

import logging
import os

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"
RUNTIME_INSTANT_MEETINGS_FILE = "runtime_instant_meetings.json"
RUNTIME_CHAT_MESSAGES_FILE = "runtime_chat_messages.json"
RUNTIME_MEETING_ACTIONS_FILE = "runtime_meeting_actions.json"

ACTION_EMOJI_REACTION = "EMOJI_REACTION"
ACTION_LOWER_HAND = "LOWER_HAND"
ACTION_MEETING_EXITED = "MEETING_EXITED"
ACTION_RAISE_HAND = "RAISE_HAND"
ACTION_MEETING_STARTED = "MEETING_STARTED"
ACTION_MEETING_MEDIA_STATE_CHANGED = "MEETING_MEDIA_STATE_CHANGED"

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "zoom", f"task_{task_id:02d}")


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
        for item in _as_list(_read_runtime_json(task_id, RUNTIME_INSTANT_MEETINGS_FILE, device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _chat_messages(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all chat messages."""
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, RUNTIME_CHAT_MESSAGES_FILE, device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _meeting_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all meeting actions."""
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, RUNTIME_MEETING_ACTIONS_FILE, device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _matching_instant_sessions(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    source: str | None = None,
    meeting_number: str | None = None,
    use_personal_meeting_id: bool | None = None,
) -> list[dict]:
    """Get instant sessions matching the given criteria."""
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


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching the predicate."""
    for item in reversed(records):
        if predicate(item):
            return item
    return None


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
    """Find a meeting action matching the given criteria."""
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
            import re
            note_text = str(action.get("note", ""))
            normalized = re.sub(r"\s+", " ", note_text).strip().lower()
            if not all(re.sub(r"\s+", " ", keyword).strip().lower() in normalized for keyword in note_keywords):
                return False
        return True

    return _find_latest(actions, predicate)


def _resolve_effective_media_state(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    meeting_id: str,
) -> dict | None:
    """Resolve the effective media state for a meeting."""
    if not meeting_id:
        return None
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
    """Check if media state matches the given criteria."""
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


def _chat_message_exists(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    meeting_ids: set[str] | None = None,
    content_exact: str | None = None,
    keyword_groups: list[list[str]] | None = None,
) -> bool:
    """Check if a chat message exists matching the given criteria."""
    import re
    normalized_exact = re.sub(r"\s+", " ", content_exact).strip().lower() if content_exact is not None else None
    for message in reversed(_chat_messages(task_id, device_id, backup_dir)):
        if str(message.get("senderId", "")) != CURRENT_USER_ID:
            continue
        if meeting_ids and str(message.get("meetingId", "")) not in meeting_ids:
            continue
        content = str(message.get("content", ""))
        if normalized_exact is not None:
            normalized_content = re.sub(r"\s+", " ", content).strip().lower()
            if normalized_content != normalized_exact:
                continue
        if keyword_groups:
            normalized_content = re.sub(r"\s+", " ", content).strip().lower()
            if not any(
                all(re.sub(r"\s+", " ", keyword).strip().lower() in normalized_content for keyword in group)
                for group in keyword_groups
            ):
                continue
        return True
    return False


def verify_copy_invite_link_then_leave(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """Verify task 3: Join meeting 994488281, mic off, camera on, chat, reactions, leave.

    Requirements:
    - Join instant meeting with number 994488281
    - Microphone off, camera on
    - Send chat message "I'm lcl."
    - Raise hand
    - Lower hand
    - Send thumbs up emoji reaction
    - Leave meeting (not end for all)
    """
    task_id = 3

    join_sessions = _matching_instant_sessions(
        task_id, device_id, backup_dir, source="JOIN", meeting_number="994488281"
    )
    join_session = join_sessions[-1] if join_sessions else None
    meeting_id = str(join_session.get("signalId", "")) if join_session else ""
    media_state = _resolve_effective_media_state(
        task_id, device_id, backup_dir, meeting_id
    )
    has_media_state = bool(meeting_id) and _media_state_matches(
        media_state, microphone_on=False, camera_on=True
    )
    has_chat = bool(meeting_id) and _chat_message_exists(
        task_id,
        device_id,
        backup_dir,
        meeting_ids={meeting_id},
        content_exact="I'm lcl.",
    )
    has_raise_hand = bool(meeting_id) and _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_RAISE_HAND,
        meeting_id=meeting_id,
    ) is not None
    has_lower_hand = bool(meeting_id) and _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_LOWER_HAND,
        meeting_id=meeting_id,
    ) is not None
    has_thumbs_up = bool(meeting_id) and _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_EMOJI_REACTION,
        meeting_id=meeting_id,
        emoji="\U0001f44d",
    ) is not None
    has_leave_self = bool(meeting_id) and _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_MEETING_EXITED,
        meeting_id=meeting_id,
        exit_action="LEAVE_SELF",
    ) is not None

    return bool(
        join_session
        and has_media_state
        and has_chat
        and has_raise_hand
        and has_lower_hand
        and has_thumbs_up
        and has_leave_self
    )


if __name__ == "__main__":
    print(verify_copy_invite_link_then_leave())

