import logging
import re

try:
    from ._device_utils import (
        contains_text,
        current_ui_text,
        default_backup_dir,
        list_records,
        normalize_text,
        read_clipboard_text,
        read_json_from_device,
    )
except ImportError:
    from _device_utils import (
        contains_text,
        current_ui_text,
        default_backup_dir,
        list_records,
        normalize_text,
        read_clipboard_text,
        read_json_from_device,
    )


PACKAGE_NAME = "com.example.tencent_meeting_sim"
USER_ID = "user001"
MEETING_ID = "4157555988"
EXPECTED_LINK = "meeting.tencent.com/p/4157555988"
ROOMS_FILE = "personal_meeting_rooms.json"
LAST_COPIED_LINK_FILE = "last_copied_link.json"
CLIPBOARD_ACTIONS_FILE = "clipboard_actions.json"
COPY_ACTION_TYPE = "personal_room_link"
COPY_SUCCESS_MARKERS = [
    "Copied",
    "Link copied",
    "Copied to clipboard",
    "\u94fe\u63a5\u5df2\u590d\u5236",
    "\u590d\u5236\u6210\u529f",
    "\u5df2\u590d\u5236",
]
CLIPBOARD_UNREADABLE_MARKERS = [
    "securityexception",
    "permission denial",
    "permission denied",
    "access denied",
    "can't find service",
    "unknown command",
    "not found",
    "no primary clip",
    "no clip",
    "primaryclip=null",
    "primary clip: null",
    "clipboard is empty",
    "service not found",
]


def _room_data_has_expected_link(device_id, backup_dir) -> bool:
    rooms = list_records(
        read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{ROOMS_FILE}",
            backup_dir=backup_dir,
        )
    )
    return any(
        str(room.get("userId")) == USER_ID
        and str(room.get("meetingId")) == MEETING_ID
        and EXPECTED_LINK.casefold() in str(room.get("meetingLink", "")).casefold()
        for room in rooms
    )


def _text_has_expected_link(value: str) -> bool:
    compact_text = re.sub(r"\s+", "", str(value or "")).casefold()
    return bool(re.search(rf"(?:https?://)?{re.escape(EXPECTED_LINK.casefold())}", compact_text))


def _copy_record_matches(record) -> bool:
    if not isinstance(record, dict):
        return False
    return (
        str(record.get("userId")) == USER_ID
        and str(record.get("type")) == COPY_ACTION_TYPE
        and _text_has_expected_link(record.get("text"))
        and record.get("timestamp") is not None
    )


def _records_from_data(data) -> list[dict]:
    if isinstance(data, dict):
        return [data]
    return list_records(data)


def _read_optional_file(device_id, backup_dir, file_name):
    return read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{file_name}",
        backup_dir=backup_dir,
        required=False,
    )


def _latest_relevant_record(records: list[dict]) -> dict | None:
    relevant_records = [
        record for record in records
        if str(record.get("userId")) == USER_ID and str(record.get("type")) == COPY_ACTION_TYPE
    ]
    if not relevant_records:
        return None
    return max(relevant_records, key=_record_timestamp)


def _record_timestamp(record: dict) -> int:
    try:
        return int(record.get("timestamp") or 0)
    except (TypeError, ValueError):
        return 0


def _copy_record_status(device_id, backup_dir) -> bool | None:
    last_record_data = _read_optional_file(device_id, backup_dir, LAST_COPIED_LINK_FILE)
    if last_record_data is not None:
        records = _records_from_data(last_record_data)
        if records:
            return any(_copy_record_matches(record) for record in records)
        return False

    actions_data = _read_optional_file(device_id, backup_dir, CLIPBOARD_ACTIONS_FILE)
    if actions_data is None:
        return None

    latest_record = _latest_relevant_record(_records_from_data(actions_data))
    if latest_record is None:
        return False
    return _copy_record_matches(latest_record)


def _clipboard_has_expected_link(clipboard_text: str) -> bool:
    return _text_has_expected_link(clipboard_text)


def _clipboard_sections(clipboard_text: str) -> list[tuple[str, str]]:
    return re.findall(r"(?ms)^--- (.*?) ---\n(.*?)(?=^--- .*? ---\n|\Z)", clipboard_text or "")


def _clipboard_read_unavailable(clipboard_text: str) -> bool:
    normalized = normalize_text(clipboard_text).casefold()
    if not normalized:
        return True

    sections = _clipboard_sections(clipboard_text)
    if not sections:
        return any(marker in normalized for marker in CLIPBOARD_UNREADABLE_MARKERS)

    saw_unreadable_output = False
    for label, content in sections:
        section = normalize_text(content).casefold()
        if not section:
            continue
        if any(marker in section for marker in CLIPBOARD_UNREADABLE_MARKERS):
            saw_unreadable_output = True
            continue
        if label.startswith("cmd clipboard") or label.endswith("decoded utf16"):
            return False
        if label == "dumpsys clipboard" and any(marker in section for marker in ("text=", "text:", "clipdata")):
            return False
        if label.startswith("service call clipboard") and "result: parcel" in section:
            saw_unreadable_output = True

    return saw_unreadable_output


def _ui_has_copy_success_evidence(device_id, backup_dir) -> bool:
    ui_text = current_ui_text(device_id, backup_dir)
    if not ui_text:
        return False
    return contains_text(ui_text, [EXPECTED_LINK]) and contains_text(ui_text, COPY_SUCCESS_MARKERS)


def verify_invitation_link_copied(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """Verify the target personal meeting room link was copied."""

    del result
    if backup_dir is None:
        backup_dir = default_backup_dir("tencentmeeting_eval_7")

    room_ok = _room_data_has_expected_link(device_id, backup_dir)
    if not room_ok:
        logging.error("Personal room data does not contain expected link %s.", EXPECTED_LINK)
        return False

    copy_record_status = _copy_record_status(device_id, backup_dir)
    if copy_record_status is True:
        logging.info("App private copy record contains expected personal room link.")
        return True
    if copy_record_status is False:
        logging.error("App private copy record does not contain expected link %s.", EXPECTED_LINK)
        return False

    clipboard_text = read_clipboard_text(device_id, backup_dir)
    if not _clipboard_has_expected_link(clipboard_text):
        if _clipboard_read_unavailable(clipboard_text) and _ui_has_copy_success_evidence(device_id, backup_dir):
            logging.info("Clipboard was unreadable, but current UI shows the expected link and copy success.")
            return True
        logging.error("Clipboard does not contain expected link %s.", EXPECTED_LINK)
        return False
    return True


if __name__ == "__main__":
    print(verify_invitation_link_copied())
