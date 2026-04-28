import logging
import os

try:
    from ._device_utils import contains_text, current_ui_text, default_backup_dir
except ImportError:
    from _device_utils import contains_text, current_ui_text, default_backup_dir


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


def check_search_user_by_phone(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """Verify the current UI is Chen Siyuan's contact details page."""

    del result
    if backup_dir is None:
        backup_dir = default_backup_dir("tencentmeeting_eval_6")

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


if __name__ == "__main__":
    print(check_search_user_by_phone())
