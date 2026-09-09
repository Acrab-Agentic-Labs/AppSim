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


def _tomorrow_local_date() -> date:
    """Get tomorrow's date in local timezone."""
    return datetime.now(SHANGHAI_TZ).date() + timedelta(days=1)


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


def _extract_result_answer_text(result) -> str:
    """Extract answer text from result."""
    import re
    if isinstance(result, dict):
        extracted_answer = result.get("extracted_answer")
        if isinstance(extracted_answer, dict):
            for value in extracted_answer.values():
                if value is None:
                    continue
                text = str(value).strip()
                if text:
                    return text

    if not isinstance(result, dict):
        return ""
    for key in ("final_message", "final_answer", "answer", "content", "message"):
        value = result.get(key)
        if isinstance(value, str) and value.strip():
            text = value.strip()
            tag_match = re.search(r"<ans>\s*(.*?)\s*</ans>", text, re.IGNORECASE | re.DOTALL)
            return tag_match.group(1).strip() if tag_match else text
    return ""


def _result_answer_is_arabic_number(result, expected_number: int) -> bool:
    """Check if result answer is an Arabic number matching expected."""
    import re
    answer_text = _extract_result_answer_text(result)
    if not answer_text:
        return False
    normalized = answer_text.strip()
    if not re.fullmatch(r"\d+", normalized):
        return False
    try:
        return int(normalized) == int(expected_number)
    except Exception:
        return False


TASK17_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the count of not-started meetings in the next 7 days.",
    "properties": {
        "meeting_count": {
            "type": "integer",
            "minimum": 0,
            "description": "The number of not-started meetings in the next 7 days, as an Arabic numeral integer.",
        }
    },
    "required": ["meeting_count"],
    "additionalProperties": False,
}


def verify_delay_tomorrow_noon_to_1300(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Task 19: Count not-started meetings in the next 7 days and verify the latest meeting
    is renamed to '[GUIA-19] Final Review'.

    Expected behavior:
    - Count upcoming meetings in the next 7 days
    - Find the latest meeting by start time
    - Verify it has been renamed to '[GUIA-19] Final Review'
    - Return the count as an Arabic numeral integer
    """
    task_id = 19

    future_seven_days = _upcoming_unstarted_scheduled_meetings(task_id, device_id, backup_dir, days=7)
    expected_count = len(future_seven_days)
    if not _result_answer_is_arabic_number(result, expected_count):
        logging.info(
            "Zoom task 19 verify detail: answer=%r expected_number=%s",
            _extract_result_answer_text(result),
            expected_count,
        )
        return False
    if not future_seven_days:
        return False
    latest_meeting = max(future_seven_days, key=lambda item: int(item.get("startTime", 0)))
    renamed = _find_scheduled_meeting(
        task_id,
        device_id,
        backup_dir,
        lambda item: _normalize_text(str(item.get("topic", ""))) == _normalize_text("[GUIA-19] Final Review"),
    )
    return bool(renamed and str(renamed.get("signalId", "")) == str(latest_meeting.get("signalId", "")))


if __name__ == "__main__":
    print(verify_delay_tomorrow_noon_to_1300())
