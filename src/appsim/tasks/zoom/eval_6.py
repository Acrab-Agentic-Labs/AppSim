from __future__ import annotations

import os
from datetime import date, datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"
RUNTIME_SCHEDULED_MEETINGS_FILE = "runtime_scheduled_meetings.json"
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


def _scheduled_meetings(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all scheduled meetings."""
    return [
        item
        for item in _as_list(_read_runtime_json(task_id, RUNTIME_SCHEDULED_MEETINGS_FILE, device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _to_local_datetime(timestamp_ms) -> datetime | None:
    """Convert timestamp to local datetime."""
    try:
        return datetime.fromtimestamp(int(timestamp_ms) / 1000, SHANGHAI_TZ)
    except Exception:
        return None


def _matches_local_slot(timestamp_ms, target_date: date, hour: int, minute: int, tolerance_minutes: int = 1) -> bool:
    """Check if timestamp matches a specific local time slot."""
    actual = _to_local_datetime(timestamp_ms)
    if actual is None:
        return False
    target = datetime(target_date.year, target_date.month, target_date.day, hour, minute, tzinfo=SHANGHAI_TZ)
    return abs((actual - target).total_seconds()) <= tolerance_minutes * 60


def _tomorrow_local_date() -> date:
    """Get tomorrow's date in local timezone."""
    return datetime.now(SHANGHAI_TZ).date() + timedelta(days=1)


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching the predicate."""
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _find_scheduled_meeting(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    predicate,
) -> dict | None:
    """Find a scheduled meeting matching the predicate."""
    return _find_latest(_scheduled_meetings(task_id, device_id, backup_dir), predicate)


def _normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    import re
    return re.sub(r"\s+", " ", text).strip().lower()


def _meeting_topic_contains(meeting: dict, keyword: str) -> bool:
    """Check if meeting topic contains the keyword."""
    return _normalize_text(keyword) in _normalize_text(str(meeting.get("topic", "")))


def _invitee_ids(meeting: dict) -> set[str]:
    """Get invitee IDs from a meeting."""
    return {str(user_id) for user_id in _as_list(meeting.get("inviteeUserIds")) if user_id}


def _find_user_id(name: str) -> str:
    """Find user ID by name from fixture data."""
    import json
    import pathlib

    fixtures_dir = pathlib.Path(__file__).resolve().parent / "fixtures"
    with (fixtures_dir / "users.json").open("r", encoding="utf-8") as handle:
        users = json.load(handle)

    for user in users:
        if isinstance(user, dict) and str(user.get("username")) == name:
            return str(user.get("userId", ""))
    return ""


def verify_send_im_lcl_in_new_meeting(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 7: Schedule a meeting "[GUIA-07] Project Sync" for tomorrow 19:00,
    duration 90 minutes, invite Derek Stewart and Brittany Evans,
    enable waiting room, set a passcode, host video on, participant video off.

    Expected behavior:
    - Meeting topic contains: "[GUIA-07] Project Sync"
    - Start time: tomorrow at 19:00 (with 1-minute tolerance)
    - Duration: 90 minutes
    - Invitees: Derek Stewart and Brittany Evans
    - Waiting room: enabled
    - Passcode: set (non-empty)
    - Host video: on
    - Participant video: off
    """
    task_id = 7

    # Get user IDs
    derek_id = _find_user_id("Derek Stewart")
    brittany_id = _find_user_id("Brittany Evans")
    required_invitees = {derek_id, brittany_id} - {""}

    # Get tomorrow's date
    tomorrow = _tomorrow_local_date()

    # Find the scheduled meeting matching all criteria
    meeting = _find_scheduled_meeting(
        task_id,
        device_id,
        backup_dir,
        lambda item: (
            _meeting_topic_contains(item, "[GUIA-07] Project Sync")
            and _matches_local_slot(item.get("startTime"), tomorrow, 19, 0)
            and int(item.get("durationMinutes", 0)) == 90
            and required_invitees.issubset(_invitee_ids(item))
            and bool(item.get("waitingRoomEnabled"))
            and bool(str(item.get("passcode", "")).strip())
            and bool(item.get("hostVideoOn"))
            and bool(item.get("participantVideoOn")) is False
        ),
    )
    return meeting is not None


if __name__ == "__main__":
    print(verify_send_im_lcl_in_new_meeting())
