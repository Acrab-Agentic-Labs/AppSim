from __future__ import annotations

import logging
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
    import os
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


def _is_seed_meeting(signal: dict, index: int) -> bool:
    """Check if a meeting is a seed meeting with the specified index."""
    return str(signal.get("signalId", "")).endswith(f"seed_{index}")


def _find_seed_meeting(task_id: int, device_id: str | None, backup_dir: str | None, index: int) -> dict | None:
    """Find a seed meeting by index."""
    return _find_latest(_scheduled_meetings(task_id, device_id, backup_dir), lambda signal: _is_seed_meeting(signal, index))


def verify_join_994488281_with_camera(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 10: Edit seed noon meeting.

    Task requirements:
    - Seed meeting index 2 (noon meeting)
    - Start time: tomorrow at 13:00 local time
    - Duration: 240 minutes (4 hours)
    """
    task_id = 10

    # Get tomorrow's date
    tomorrow = _tomorrow_local_date()

    # Find the seed noon meeting (index 2)
    seed_noon = _find_seed_meeting(task_id, device_id, backup_dir, 2)

    # Check if the meeting was updated correctly
    updated_seed = bool(
        seed_noon
        and _matches_local_slot(seed_noon.get("startTime"), tomorrow, 13, 0)
        and int(seed_noon.get("durationMinutes", 0)) == 240
    )

    if not updated_seed:
        logging.info("Zoom task 10 verify detail: expected seed noon meeting at tomorrow 13:00 for 240 minutes")

    return updated_seed


if __name__ == "__main__":
    print(verify_join_994488281_with_camera())

