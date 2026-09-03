"""Composite task: raise hand and inspect the target contact details.

This file inlines the logic from the former atomic checks for hand raise and
phone-number contact lookup so the deleted eval_5.py/eval_6.py files are no
longer required at import time.
"""

import logging

try:
    from ._device_utils import (
        contains_text,
        current_ui_text,
        default_backup_dir,
        list_records,
        read_json_from_device,
    )
except ImportError:
    from _device_utils import (
        contains_text,
        current_ui_text,
        default_backup_dir,
        list_records,
        read_json_from_device,
    )


PACKAGE_NAME = "com.example.tencent_meeting_sim"
MEETING_ID = "meeting_3d7e91"
USER_ID = "user001"
MEETING_PARTICIPANTS_FILE = "meeting_participants.json"
HAND_RAISE_RECORDS_FILE = "hand_raise_records.json"

IS_HAND_RAISED_KEY = "isHandRaised"
MEETING_ID_KEY = "meetingId"
USER_ID_KEY = "userId"
LOWER_TIME_KEY = "lowerTime"

TARGET_NAME = "\u9648\u601d\u8fdc"
TARGET_PHONE = "15823467912"
DETAIL_PAGE_MARKERS = [
    "Contact Method",
    "Email",
    "Call",
    "Source",
    "Added via meeting",
    "\u8054\u7cfb\u65b9\u5f0f",
    "\u90ae\u7bb1",
    "\u547c\u53eb",
    "\u6765\u6e90",
    "\u901a\u8fc7\u4f1a\u8bae\u6dfb\u52a0",
]


def _check_hand_raise(result=None, device_id=None, backup_dir=None) -> bool:
    participants_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{MEETING_PARTICIPANTS_FILE}",
        backup_dir=backup_dir,
    )
    if participants_data is None:
        logging.error("Unable to read or parse %s.", MEETING_PARTICIPANTS_FILE)
        return False

    hand_raise_data = read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{HAND_RAISE_RECORDS_FILE}",
        backup_dir=backup_dir,
    )
    if hand_raise_data is None:
        logging.error("Unable to read or parse %s.", HAND_RAISE_RECORDS_FILE)
        return False

    participant_raised = any(
        record.get(MEETING_ID_KEY) == MEETING_ID
        and record.get(USER_ID_KEY) == USER_ID
        and record.get(IS_HAND_RAISED_KEY) is True
        for record in list_records(participants_data)
    )
    record_exists = any(
        record.get(MEETING_ID_KEY) == MEETING_ID
        and record.get(USER_ID_KEY) == USER_ID
        and record.get(LOWER_TIME_KEY) is None
        for record in list_records(hand_raise_data)
    )

    if not participant_raised:
        logging.error(
            "User %s is not marked as hand-raised in meeting %s.",
            USER_ID,
            MEETING_ID,
        )
    if not record_exists:
        logging.error(
            "No active hand-raise record found for user %s in meeting %s.",
            USER_ID,
            MEETING_ID,
        )

    if not (participant_raised and record_exists) and isinstance(result, dict):
        executed_actions = result.get("executed_actions", [])
        hand_raise_clicked = any(
            action.get("action") == "click"
            and "\u4e3e\u624b" in str(action.get("description", ""))
            for action in executed_actions
            if isinstance(action, dict)
        )
        if hand_raise_clicked:
            logging.warning("Data was not updated, but executed actions show a hand-raise click.")
            return True

    return participant_raised and record_exists


def _check_search_user_by_phone(device_id=None, backup_dir=None) -> bool:
    ui_text = current_ui_text(device_id, backup_dir)
    if not ui_text:
        logging.error("Unable to read current UI state.")
        return False

    has_name = contains_text(ui_text, [TARGET_NAME, "Chen Siyuan"])
    has_phone = contains_text(ui_text, [TARGET_PHONE])
    has_detail_context = contains_text(ui_text, DETAIL_PAGE_MARKERS)

    if not has_name:
        logging.error("Current UI does not show target contact name Chen Siyuan.")
    if not has_phone:
        logging.error("Current UI does not show target phone %s.", TARGET_PHONE)
    if not has_detail_context:
        logging.error("Current UI does not show contact-detail fields.")
    return has_name and has_phone and has_detail_context


def _run_subcheck(label, verify_func, *args, **kwargs) -> bool:
    try:
        return bool(verify_func(*args, **kwargs))
    except Exception:
        logging.exception("Composite eval_25 subcheck raised an exception: %s.", label)
        return False


def verify_hand_raise_and_contact_lookup(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """Verify hand raise in the meeting and the target phone contact page."""

    if kwargs:
        logging.debug("Composite eval_25 ignored extra args: %s", sorted(kwargs))
    if backup_dir is None:
        backup_dir = default_backup_dir("tencentmeeting_eval_25")

    hand_raise_ok = _run_subcheck(
        "hand raise",
        _check_hand_raise,
        result=result,
        device_id=device_id,
        backup_dir=backup_dir,
    )
    search_user_ok = _run_subcheck(
        "phone contact details",
        _check_search_user_by_phone,
        device_id=device_id,
        backup_dir=backup_dir,
    )

    if hand_raise_ok:
        logging.info("Composite eval_25 subcheck passed: hand raise.")
    else:
        logging.error("Composite eval_25 subcheck failed: hand raise.")

    if search_user_ok:
        logging.info("Composite eval_25 subcheck passed: phone contact details.")
    else:
        logging.error("Composite eval_25 subcheck failed: phone contact details.")

    return hand_raise_ok and search_user_ok


if __name__ == "__main__":
    print(verify_hand_raise_and_contact_lookup())
