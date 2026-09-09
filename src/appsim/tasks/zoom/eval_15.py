from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"
RUNTIME_SCHEDULED_MEETINGS_FILE = "runtime_scheduled_meetings.json"
RUNTIME_INSTANT_MEETINGS_FILE = "runtime_instant_meetings.json"
RUNTIME_MEETING_PREFERENCES_FILE = "runtime_meeting_preferences.json"
RUNTIME_MEETING_ACTIONS_FILE = "runtime_meeting_actions.json"

ACTION_MEETING_STARTED = "MEETING_STARTED"
ACTION_MEETING_MEDIA_STATE_CHANGED = "MEETING_MEDIA_STATE_CHANGED"

SHANGHAI_TZ = timezone(timedelta(hours=8))

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


def _as_dict(value) -> dict:
    """Convert value to dict if possible."""
    return value if isinstance(value, dict) else {}


def _instant_meetings(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all instant meetings."""
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, RUNTIME_INSTANT_MEETINGS_FILE, device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _meeting_preferences(task_id: int, device_id: str | None, backup_dir: str | None) -> dict:
    """Get meeting preferences."""
    return _as_dict(_read_runtime_json(task_id, RUNTIME_MEETING_PREFERENCES_FILE, device_id, backup_dir))


def _meeting_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all meeting actions."""
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, RUNTIME_MEETING_ACTIONS_FILE, device_id, backup_dir))
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
    """Find a single instant session matching criteria."""
    matches = _matching_instant_sessions(
        task_id,
        device_id,
        backup_dir,
        source=source,
        meeting_number=meeting_number,
        use_personal_meeting_id=use_personal_meeting_id,
    )
    return matches[-1] if matches else None


def _resolve_effective_media_state(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    meeting_id: str,
) -> dict | None:
    """Resolve the effective media state for a meeting."""
    if not meeting_id:
        return None

    # Find latest media state change action
    latest_media_change = None
    for action in reversed(_meeting_actions(task_id, device_id, backup_dir)):
        if str(action.get("actionType", "")) == ACTION_MEETING_MEDIA_STATE_CHANGED:
            if str(action.get("meetingId", "")) == meeting_id:
                latest_media_change = action
                break

    if latest_media_change is not None:
        return latest_media_change

    # Fall back to meeting started action
    for action in reversed(_meeting_actions(task_id, device_id, backup_dir)):
        if str(action.get("actionType", "")) == ACTION_MEETING_STARTED:
            if str(action.get("meetingId", "")) == meeting_id:
                return action

    return None


def _media_state_matches(
    media_state: dict | None,
    *,
    microphone_on: bool | None = None,
    camera_on: bool | None = None,
    audio_option: str | None = None,
    media_change_source: str | None = None,
) -> bool:
    """Check if media state matches specified criteria."""
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


def verify_cancel_may_first_schedule(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 17: Start instant meeting with specific preferences.

    This task evaluates:
    1. An instant meeting was hosted
    2. Meeting preferences: autoConnectAudioOn is False
    3. Meeting preferences: autoTurnOnCameraOn is True
    4. Effective media state: camera is on, audio option is "none"
    """
    task_id = 17

    preferences = _meeting_preferences(task_id, device_id, backup_dir)
    host_session = _find_instant_session(task_id, device_id, backup_dir, source="HOST")
    meeting_id = str(host_session.get("signalId", "")) if host_session else ""
    media_state = _resolve_effective_media_state(task_id, device_id, backup_dir, meeting_id)
    return bool(
        host_session
        and preferences.get("autoConnectAudioOn") is False
        and preferences.get("autoTurnOnCameraOn") is True
        and _media_state_matches(media_state, camera_on=True, audio_option="none")
    )


if __name__ == "__main__":
    print(verify_cancel_may_first_schedule())

