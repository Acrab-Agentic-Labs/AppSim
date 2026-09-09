from __future__ import annotations

import json
import logging
import os
import pathlib
from datetime import date, datetime, timedelta, timezone
from functools import lru_cache

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"
RUNTIME_SCHEDULED_MEETINGS_FILE = "runtime_scheduled_meetings.json"
FIXTURES_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "zoom", f"task_{task_id:02d}")


def _load_fixture_json(filename: str):
    """Load a JSON fixture file."""
    with (FIXTURES_DIR / filename).open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _fixture_context() -> dict:
    """Load and cache user fixture data."""
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


def _day_after_tomorrow_local_date() -> date:
    """Get day after tomorrow's date in local timezone."""
    return datetime.now(SHANGHAI_TZ).date() + timedelta(days=2)


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


def _meeting_topic_contains(meeting: dict, keyword: str) -> bool:
    """Check if meeting topic contains a keyword."""
    import re
    def _normalize_text(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip().lower()
    return _normalize_text(keyword) in _normalize_text(str(meeting.get("topic", "")))


def _invitee_ids(meeting: dict) -> set[str]:
    """Extract invitee user IDs from a meeting."""
    return {str(user_id) for user_id in _as_list(meeting.get("inviteeUserIds")) if user_id}


def verify_busy_status(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 8: Schedule a recurring weekday meeting.

    Expected behavior:
    - Meeting topic contains "[GUIA-08] Daily Standup"
    - Start time: day after tomorrow at 09:30 (9:30 AM)
    - Duration: 30 minutes
    - Recurrence: Every weekday
    - Invitees: Amber Campbell and Natalie Cox
    - Join before host disabled (allowJoinBeforeHost is False)
    """
    # Get user IDs for required invitees
    amber_id = _find_user_id("Amber Campbell")
    natalie_id = _find_user_id("Natalie Cox")
    required_invitees = {amber_id, natalie_id} - {""}

    # Get day after tomorrow's date
    day_after_tomorrow = _day_after_tomorrow_local_date()

    # Find the scheduled meeting matching task 8 criteria
    meeting = _find_scheduled_meeting(
        task_id=7,
        device_id=device_id,
        backup_dir=backup_dir,
        predicate=lambda item: (
            _meeting_topic_contains(item, "[GUIA-08] Daily Standup")
            and _matches_local_slot(item.get("startTime"), day_after_tomorrow, 9, 30)
            and int(item.get("durationMinutes", 0)) == 30
            and str(item.get("repeat", "")) == "Every weekday"
            and required_invitees.issubset(_invitee_ids(item))
            and bool(item.get("allowJoinBeforeHost", True)) is False
        ),
    )

    return meeting is not None


if __name__ == "__main__":
    print(verify_busy_status())

