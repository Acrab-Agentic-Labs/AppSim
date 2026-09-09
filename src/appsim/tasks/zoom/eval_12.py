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
RUNTIME_MEETING_ACTIONS_FILE = "runtime_meeting_actions.json"
ACTION_COPY_INVITE_LINK = "COPY_INVITE_LINK"
SHANGHAI_TZ = timezone(timedelta(hours=8))

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}

TASK12_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the count of not-started scheduled meetings.",
    "properties": {
        "meeting_count": {
            "type": "integer",
            "minimum": 0,
            "description": "The number of not-started scheduled meetings, as an Arabic numeral integer.",
        }
    },
    "required": ["meeting_count"],
    "additionalProperties": False,
}


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


def _normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    return re.sub(r"\s+", " ", text).strip().lower()


def _extract_result_answer_text(result) -> str:
    """Extract answer text from result."""
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
    """Check if result answer is an arabic number matching expected."""
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


def _text_contains_all(text: str, keywords: list[str]) -> bool:
    """Check if text contains all keywords."""
    normalized = _normalize_text(text)
    return all(_normalize_text(keyword) in normalized for keyword in keywords)


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
    """Find a meeting action matching the criteria."""
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


def verify_contact_count_answer(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 13: Check upcoming meetings count and copy invite link action.

    Returns True if the answer matches the expected count of upcoming meetings
    and the invite link was copied for the earliest meeting.
    """
    task_id = 13

    upcoming = _upcoming_unstarted_scheduled_meetings(task_id, device_id, backup_dir)
    expected_count = len(upcoming)
    if not _result_answer_is_arabic_number(result, expected_count):
        logging.info(
            "Zoom task 13 verify detail: answer=%r expected_number=%s",
            _extract_result_answer_text(result),
            expected_count,
        )
        return False
    if not upcoming:
        return False
    earliest = min(upcoming, key=lambda item: int(item.get("startTime", 0)))
    return _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_COPY_INVITE_LINK,
        meeting_id=str(earliest.get("signalId", "")),
    ) is not None


if __name__ == "__main__":
    print(verify_contact_count_answer())

