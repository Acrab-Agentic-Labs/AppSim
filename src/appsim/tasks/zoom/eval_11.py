from __future__ import annotations

import logging
from datetime import datetime, timedelta, timezone

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


def _meeting_topic_contains(meeting: dict, keyword: str) -> bool:
    """Check if meeting topic contains keyword."""
    import re
    def normalize_text(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip().lower()
    return normalize_text(keyword) in normalize_text(str(meeting.get("topic", "")))


def verify_raise_lower_hand_with_thumbs_up(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    task_id = 12
    may_first_guia_meetings = [
        meeting
        for meeting in _scheduled_meetings(task_id, device_id, backup_dir)
        if _meeting_topic_contains(meeting, "[GUIA]")
        and (_to_local_datetime(meeting.get("startTime")) is not None)
        and _to_local_datetime(meeting.get("startTime")).month == 5
        and _to_local_datetime(meeting.get("startTime")).day == 1
    ]
    if may_first_guia_meetings:
        logging.info("Zoom task 12 verify detail: May 1 [GUIA] meetings still exist: %s", len(may_first_guia_meetings))
        return False
    return True


if __name__ == "__main__":
    print(verify_raise_lower_hand_with_thumbs_up())
