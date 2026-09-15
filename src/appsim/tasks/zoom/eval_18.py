from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
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


def _upcoming_unstarted_scheduled_meetings(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    days: int | None = None,
) -> list[dict]:
    """Get upcoming unstarted scheduled meetings."""
    now = datetime.now(SHANGHAI_TZ)
    meetings = []
    for meeting in _scheduled_meetings(task_id, device_id, backup_dir):
        start_at = _to_local_datetime(meeting.get("startTime"))
        if start_at is None:
            continue
        if start_at <= now:
            continue
        if days is not None and start_at > now + timedelta(days=days):
            continue
        meetings.append(meeting)
    return meetings


def verify_enable_waiting_room_and_extend_noon_meeting(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 20: Enable waiting room and disable 'allow join before host' for the nearest upcoming meeting.

    Checks:
    - Find the nearest upcoming unstarted scheduled meeting
    - Verify waiting room is enabled
    - Verify allow join before host is disabled (False)
    """
    future_meetings = _upcoming_unstarted_scheduled_meetings(20, device_id, backup_dir)
    if not future_meetings:
        return False
    nearest = min(future_meetings, key=lambda item: int(item.get("startTime", 0)))
    passed = bool(nearest.get("waitingRoomEnabled")) and bool(nearest.get("allowJoinBeforeHost", True)) is False
    return passed


if __name__ == "__main__":
    print(verify_enable_waiting_room_and_extend_noon_meeting())
