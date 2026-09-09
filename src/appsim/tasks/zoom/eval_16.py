"""
Verification logic for Zoom task 16.
Checks if PMI meeting is hosted, invite link copied, sent to Amber, and meeting not ended.
"""

from __future__ import annotations

import json
import logging
import os
import pathlib
import re
import subprocess
from functools import lru_cache

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
CURRENT_USER_ID = "user001"
PERSONAL_MEETING_NUMBER = "9948881080"

# Runtime files
RUNTIME_INSTANT_MEETINGS_FILE = "runtime_instant_meetings.json"
RUNTIME_DIRECT_MESSAGES_FILE = "runtime_direct_messages.json"
RUNTIME_MEETING_ACTIONS_FILE = "runtime_meeting_actions.json"
RUNTIME_CLIPBOARD_ACTIONS_FILE = "runtime_clipboard_actions.json"

# Action constants
ACTION_MEETING_EXITED = "MEETING_EXITED"
ACTION_COPY_INVITE_LINK = "COPY_INVITE_LINK"

# Keyword groups
INVITE_LINK_PREFIX_KEYWORD_GROUPS = [['use this link', 'join the meeting']]

# Fixtures
FIXTURES_DIR = pathlib.Path(__file__).resolve().parent / "fixtures"

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "zoom", f"task_{task_id:02d}")


def _load_fixture_json(filename: str):
    """Load a fixture JSON file."""
    with (FIXTURES_DIR / filename).open("r", encoding="utf-8") as handle:
        return json.load(handle)


@lru_cache(maxsize=1)
def _fixture_context() -> dict:
    """Load and cache fixture context including users."""
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


def _read_optional_runtime_json(task_id: int, filename: str, device_id: str | None, backup_dir: str | None):
    """Read optional runtime JSON, returns None if unavailable."""
    cache_key = (task_id, filename, device_id, backup_dir)
    if cache_key not in _RUNTIME_CACHE:
        try:
            _RUNTIME_CACHE[cache_key] = _read_runtime_json(task_id, filename, device_id, backup_dir)
        except Exception as exc:
            logging.info("Optional Zoom runtime file %s is unavailable: %s", filename, exc)
            _RUNTIME_CACHE[cache_key] = None
    return _RUNTIME_CACHE[cache_key]


def _as_list(value) -> list:
    """Convert value to list if possible."""
    return value if isinstance(value, list) else []


def _instant_meetings(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all instant meetings."""
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_INSTANT_MEETINGS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _direct_messages(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all direct messages."""
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_DIRECT_MESSAGES_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _meeting_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all meeting actions."""
    return [item for item in _as_list(_read_runtime_json(task_id, RUNTIME_MEETING_ACTIONS_FILE, device_id, backup_dir)) if isinstance(item, dict)]


def _clipboard_actions(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get all clipboard actions."""
    return [
        item
        for item in _as_list(_read_optional_runtime_json(task_id, RUNTIME_CLIPBOARD_ACTIONS_FILE, device_id, backup_dir))
        if isinstance(item, dict)
    ]


def _normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    return re.sub(r"\s+", " ", text).strip().lower()


def _compact_digits(text: str) -> str:
    """Extract all digits from text."""
    return re.sub(r"\D+", "", str(text or ""))


def _text_contains_all(text: str, keywords: list[str]) -> bool:
    """Check if text contains all keywords."""
    normalized = _normalize_text(text)
    return all(_normalize_text(keyword) in normalized for keyword in keywords)


def _text_matches_groups(text: str, groups: list[list[str]]) -> bool:
    """Check if text matches any keyword group."""
    normalized = _normalize_text(text)
    return any(all(_normalize_text(keyword) in normalized for keyword in group) for group in groups)


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
    use_personal_meeting_id: bool | None = None
) -> list[dict]:
    """Find all instant sessions matching criteria."""
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
    """Find the latest instant session matching criteria."""
    matches = _matching_instant_sessions(
        task_id,
        device_id,
        backup_dir,
        source=source,
        meeting_number=meeting_number,
        use_personal_meeting_id=use_personal_meeting_id,
    )
    return matches[-1] if matches else None


def _adb_command(device_id: str | None, *args: str) -> list[str]:
    """Build ADB command."""
    command = [os.environ.get("ADBUTILS_ADB_PATH") or "adb"]
    if device_id:
        command.extend(["-s", str(device_id)])
    command.extend(str(arg) for arg in args)
    return command


def _read_clipboard_text(device_id: str | None, backup_dir: str | None) -> str:
    """Read clipboard text from device."""
    commands: list[tuple[str, tuple[str, ...]]] = [
        ("cmd clipboard get", ("shell", "cmd", "clipboard", "get")),
        ("cmd clipboard get --user 0", ("shell", "cmd", "clipboard", "get", "--user", "0")),
        ("dumpsys clipboard", ("shell", "dumpsys", "clipboard")),
    ]
    chunks: list[str] = []
    for label, args in commands:
        try:
            result = subprocess.run(
                _adb_command(device_id, *args),
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=10.0,
            )
        except Exception as exc:
            logging.info("Unable to read Zoom clipboard using %s: %s", label, exc)
            continue
        output = f"{result.stdout}\n{result.stderr}".strip()
        if output:
            chunks.append(f"--- {label} ---\n{output}")

    clipboard_text = "\n".join(chunks)
    if backup_dir:
        try:
            backup_path = pathlib.Path(backup_dir)
            backup_path.mkdir(parents=True, exist_ok=True)
            (backup_path / "clipboard.txt").write_text(clipboard_text, encoding="utf-8")
        except Exception as exc:
            logging.info("Unable to write Zoom clipboard backup: %s", exc)
    return clipboard_text


def _text_has_invite_link(text: str, meeting_number: str | None = None) -> bool:
    """Check if text contains a Zoom invite link."""
    normalized = str(text or "").lower()
    if "zoom.us/j/" not in normalized:
        return False
    if meeting_number:
        return str(meeting_number) in _compact_digits(normalized)
    return True


def _private_clipboard_has_invite_link(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    meeting_id: str,
    meeting_number: str,
) -> bool:
    """Check if clipboard actions contain invite link."""
    for action in reversed(_clipboard_actions(task_id, device_id, backup_dir)):
        action_type = str(action.get("type", action.get("actionType", "")))
        if action_type != ACTION_COPY_INVITE_LINK:
            continue
        if meeting_id and str(action.get("meetingId", "")) != meeting_id:
            continue
        if meeting_number and str(action.get("meetingNumber", "")) not in ("", meeting_number):
            continue
        if _text_has_invite_link(str(action.get("text", "")), meeting_number):
            return True
    return False


def _find_meeting_action(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    action_type: str,
    meeting_id: str | None = None,
    meeting_number: str | None = None,
    exit_action: str | None = None,
) -> dict | None:
    """Find a meeting action matching criteria."""
    actions = _meeting_actions(task_id, device_id, backup_dir)

    def predicate(action: dict) -> bool:
        if str(action.get("actionType", "")) != action_type:
            return False
        if meeting_id and str(action.get("meetingId", "")) != str(meeting_id):
            return False
        if meeting_number and str(action.get("meetingNumber", "")) != str(meeting_number):
            return False
        if exit_action is not None and str(action.get("exitAction", "")) != exit_action:
            return False
        return True

    return _find_latest(actions, predicate)


def _has_copied_invite_link(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    meeting_id: str,
    meeting_number: str,
) -> bool:
    """Check if invite link was copied."""
    if _private_clipboard_has_invite_link(
        task_id,
        device_id,
        backup_dir,
        meeting_id=meeting_id,
        meeting_number=meeting_number,
    ):
        return True

    clipboard_text = _read_clipboard_text(device_id, _build_backup_dir(task_id, backup_dir))
    if _text_has_invite_link(clipboard_text, meeting_number):
        return True

    legacy_action = _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_COPY_INVITE_LINK,
        meeting_id=meeting_id,
    )
    return legacy_action is not None


def _direct_message_exists(
    task_id: int,
    device_id: str | None,
    backup_dir: str | None,
    *,
    partner_user_id: str,
    keyword_groups: list[list[str]] | None = None,
    require_link: bool = False,
) -> bool:
    """Check if a direct message exists matching criteria."""
    for message in reversed(_direct_messages(task_id, device_id, backup_dir)):
        if str(message.get("senderId", "")) != CURRENT_USER_ID:
            continue
        if str(message.get("partnerUserId", "")) != str(partner_user_id):
            continue
        content = str(message.get("content", ""))
        if keyword_groups and not _text_matches_groups(content, keyword_groups):
            continue
        if require_link and "https://zoom.us/j/" not in content.lower():
            continue
        return True
    return False


def verify_message_natalie_about_next_monday_leave(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 18: Host PMI meeting, copy invite link, send to Amber, keep meeting open.

    Checks:
    - Host session with personal meeting ID
    - Invite link copied
    - Direct message sent to Amber with invite link keywords
    - Meeting not ended for all

    Args:
        result: The result from task execution (unused for this task)
        device_id: Optional device ID to read data from
        backup_dir: Optional backup directory path
        **kwargs: Additional keyword arguments (unused)

    Returns:
        bool: True if all conditions are met, False otherwise
    """
    task_id = 18
    amber_id = _find_user_id("Amber Campbell")

    host_session = _find_instant_session(
        task_id,
        device_id,
        backup_dir,
        source="HOST",
        meeting_number=PERSONAL_MEETING_NUMBER,
        use_personal_meeting_id=True,
    )
    meeting_id = str(host_session.get("signalId", "")) if host_session else ""

    has_host_session = bool(host_session)
    has_copied_link = bool(
        host_session
        and _has_copied_invite_link(
            task_id,
            device_id,
            backup_dir,
            meeting_id=meeting_id,
            meeting_number=PERSONAL_MEETING_NUMBER,
        )
    )
    has_sent_to_amber = bool(
        amber_id
        and _direct_message_exists(
            task_id,
            device_id,
            backup_dir,
            partner_user_id=amber_id,
            keyword_groups=INVITE_LINK_PREFIX_KEYWORD_GROUPS,
            require_link=True,
        )
    )
    no_end_for_all = not _find_meeting_action(
        task_id,
        device_id,
        backup_dir,
        action_type=ACTION_MEETING_EXITED,
        meeting_id=meeting_id,
        exit_action="END_FOR_ALL",
    )

    passed = bool(
        has_host_session
        and has_copied_link
        and has_sent_to_amber
        and no_end_for_all
    )

    if not passed:
        logging.info(
            "Zoom task 18 verify detail: host_session=%s copied_link=%s sent_to_amber=%s no_end_for_all=%s meeting_id=%s amber_id=%s",
            has_host_session,
            has_copied_link,
            has_sent_to_amber,
            no_end_for_all,
            meeting_id,
            amber_id,
        )

    return passed


if __name__ == "__main__":
    print(verify_message_natalie_about_next_monday_leave())
