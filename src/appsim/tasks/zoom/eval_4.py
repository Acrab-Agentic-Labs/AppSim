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

# Action types
ACTION_MEETING_EXITED = "MEETING_EXITED"
ACTION_SCREEN_SHARE_PAUSED = "SCREEN_SHARE_PAUSED"
ACTION_SCREEN_SHARE_STATUS_CHANGED = "SCREEN_SHARE_STATUS_CHANGED"
ACTION_SCREEN_SHARE_RESUMED = "SCREEN_SHARE_RESUMED"

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
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_INSTANT_MEETINGS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _chat_messages(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all chat messages."""
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_CHAT_MESSAGES_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _meeting_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all meeting actions."""
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_MEETING_ACTIONS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching the predicate."""
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _normalize_text(text: str) -> str:
    """Normalize text by lowercasing and removing extra whitespace."""
    import re
    return re.sub(r"\s+", " ", text).strip().lower()


def _matching_instant_sessions(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    source: str | None = None,
    meeting_number: str | None = None,
    use_personal_meeting_id: bool | None = None
) -> list[dict]:
    """Find instant sessions matching the given criteria."""
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
    """Find the latest instant session matching the given criteria."""
    matches = _matching_instant_sessions(
        task_id,
        device_id,
        backup_dir,
        source=source,
        meeting_number=meeting_number,
        use_personal_meeting_id=use_personal_meeting_id,
    )
    return matches[-1] if matches else None


def _find_meeting_action(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    action_type: str,
    meeting_id: str | None = None,
    meeting_number: str | None = None,
    screen_sharing_enabled: bool | None = None,
    exit_action: str | None = None
) -> dict | None:
    """Find the latest meeting action matching the given criteria."""
    actions = _meeting_actions(task_id, device_id, backup_dir)

    def predicate(action: dict) -> bool:
        if str(action.get("actionType", "")) != action_type:
            return False
        if meeting_id and str(action.get("meetingId", "")) != str(meeting_id):
            return False
        if meeting_number and str(action.get("meetingNumber", "")) != str(meeting_number):
            return False
        if screen_sharing_enabled is not None and action.get("screenSharingEnabled") != screen_sharing_enabled:
            return False
        if exit_action is not None and str(action.get("exitAction", "")) != exit_action:
            return False
        return True

    return _find_latest(actions, predicate)


def _actions_for_meeting(task_id: int, device_id: str | None, backup_dir: str | None, meeting_id: str) -> list[dict]:
    """Get all actions for a specific meeting."""
    if not meeting_id:
        return []
    return [
        action
        for action in _meeting_actions(task_id, device_id, backup_dir)
        if str(action.get("meetingId", "")) == meeting_id
    ]


def _action_timestamp_ms(action: dict) -> int:
    """Get the timestamp of an action in milliseconds."""
    try:
        return int(action.get("occurredAt", 0))
    except Exception:
        return 0


def _has_screen_share_resume_evidence(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    meeting_id: str
) -> bool:
    """Check if there is evidence of screen share being resumed."""
    actions = _actions_for_meeting(task_id, device_id, backup_dir, meeting_id)
    if not actions:
        return False

    pause_action = _find_latest(actions, lambda item: str(item.get("actionType", "")) == ACTION_SCREEN_SHARE_PAUSED)
    if pause_action is None:
        return False
    pause_ts = _action_timestamp_ms(pause_action)

    explicit_resume = any(
        str(action.get("actionType", "")) == ACTION_SCREEN_SHARE_RESUMED and _action_timestamp_ms(action) >= pause_ts
        for action in actions
    )
    if explicit_resume:
        return True

    # Some app builds only emit "SCREEN_SHARE_STATUS_CHANGED=true" when resuming after pause.
    implicit_resume = any(
        str(action.get("actionType", "")) == ACTION_SCREEN_SHARE_STATUS_CHANGED
        and action.get("screenSharingEnabled") is True
        and _action_timestamp_ms(action) > pause_ts
        for action in actions
    )
    return implicit_resume


def _chat_message_exists(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    meeting_ids: set[str] | None = None,
    content_exact: str | None = None
) -> bool:
    """Check if a chat message with the given criteria exists."""
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


def verify_safe_driving_hello(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 5: Screen sharing workflow
    - Start an instant meeting (HOST, not PMI)
    - Start screen sharing
    - Pause screen sharing
    - Send chat message "Sharing paused."
    - Resume screen sharing
    - Stop screen sharing
    - End meeting for all
    """
    task_id = 5

    # Find the host instant meeting session (not PMI)
    host_session = _find_instant_session(
        task_id, device_id, backup_dir, source="HOST", use_personal_meeting_id=False
    )
    meeting_id = str(host_session.get("signalId", "")) if host_session else ""

    # Check if screen sharing was started
    has_started_share = (
        _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_SCREEN_SHARE_STATUS_CHANGED,
            meeting_id=meeting_id,
            screen_sharing_enabled=True,
        )
        is not None
    )

    # Check if screen sharing was paused
    has_paused_share = (
        _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_SCREEN_SHARE_PAUSED,
            meeting_id=meeting_id,
        )
        is not None
    )

    # Check if screen sharing was resumed
    has_resume_share = _has_screen_share_resume_evidence(
        task_id, device_id, backup_dir, meeting_id
    )

    # Check if chat message "Sharing paused." was sent
    has_paused_chat = _chat_message_exists(
        task_id,
        device_id,
        backup_dir,
        meeting_ids={meeting_id},
        content_exact="Sharing paused.",
    )

    # Check if screen sharing was stopped
    has_stopped_share = (
        _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_SCREEN_SHARE_STATUS_CHANGED,
            meeting_id=meeting_id,
            screen_sharing_enabled=False,
        )
        is not None
    )

    # Check if meeting was ended for all
    has_end_for_all = (
        _find_meeting_action(
            task_id,
            device_id,
            backup_dir,
            action_type=ACTION_MEETING_EXITED,
            meeting_id=meeting_id,
            exit_action="END_FOR_ALL",
        )
        is not None
    )

    # All checks must pass
    passed = bool(
        host_session
        and has_started_share
        and has_paused_share
        and has_paused_chat
        and has_resume_share
        and has_stopped_share
        and has_end_for_all
    )

    if not passed:
        logging.info(
            "Zoom task 5 verify detail: host=%s started=%s paused=%s paused_chat=%s resumed=%s stopped=%s end_for_all=%s",
            bool(host_session),
            has_started_share,
            has_paused_share,
            has_paused_chat,
            has_resume_share,
            has_stopped_share,
            has_end_for_all,
        )

    return passed


if __name__ == "__main__":
    print(verify_safe_driving_hello())

