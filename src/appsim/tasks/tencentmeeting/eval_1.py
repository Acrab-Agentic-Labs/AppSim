import logging
import os

try:
    from ._device_utils import contains_text, current_ui_text, default_backup_dir
except ImportError:
    from _device_utils import contains_text, current_ui_text, default_backup_dir


HISTORY_TITLES = [
    "Historical Meetings",
    "\u5386\u53f2\u4f1a\u8bae",
    "\u5386\u53f2\u4f1a\u8bae\u8bb0\u5f55",
]
HISTORY_SEARCH_PLACEHOLDERS = [
    "Meeting name, notes, ID, host",
    "Meeting name, notes, meeting ID, host",
    "\u4f1a\u8bae\u540d\u79f0\u3001\u4f1a\u8bae\u5907\u6ce8\u3001\u4f1a\u8bae\u53f7\u3001\u53d1\u8d77\u4eba",
    "\u4f1a\u8bae\u540d\u79f0\u3001\u4f1a\u8bae\u5907\u6ce8\u3001ID\u3001\u53d1\u8d77\u4eba",
    "\u4f1a\u8bae\u540d\u79f0\u3001\u4f1a\u8bae\u5907\u6ce8\u3001\u4f1a\u8bae\u53f7\u3001\u4e3b\u6301\u4eba",
    "\u4f1a\u8bae\u540d\u79f0\u3001\u4f1a\u8bae\u5907\u6ce8\u3001ID\u3001\u4e3b\u6301\u4eba",
]
HISTORY_EMPTY_MARKERS = [
    "No historical meetings",
    "No meeting history",
    "No history meetings",
    "\u6682\u65e0\u5386\u53f2\u4f1a\u8bae",
    "\u6682\u65e0\u4f1a\u8bae\u8bb0\u5f55",
    "\u6ca1\u6709\u5386\u53f2\u4f1a\u8bae",
]
HISTORY_HOST_MARKERS = [
    "Host:",
    "Host",
    "\u53d1\u8d77\u4eba",
    "\u4e3b\u6301\u4eba",
]
HISTORY_TIME_MARKERS = [
    "Time:",
    "Meeting time",
    "End Time",
    "\u4f1a\u8bae\u65f6\u95f4",
    "\u7ed3\u675f\u65f6\u95f4",
    "\u65f6\u95f4",
]
HOME_PAGE_MARKERS = [
    "Meeting List",
    "Join Meeting",
    "Quick Meeting",
    "Scheduled Meeting",
    "\u4f1a\u8bae\u5217\u8868",
    "\u52a0\u5165\u4f1a\u8bae",
    "\u5feb\u901f\u4f1a\u8bae",
    "\u9884\u5b9a\u4f1a\u8bae",
]


def _has_history_page_evidence(ui_text: str) -> bool:
    has_search_placeholder = contains_text(ui_text, HISTORY_SEARCH_PLACEHOLDERS)
    has_empty_state = contains_text(ui_text, HISTORY_EMPTY_MARKERS)
    has_ended_card_fields = contains_text(ui_text, HISTORY_HOST_MARKERS) and contains_text(
        ui_text, HISTORY_TIME_MARKERS
    )
    return has_search_placeholder or has_empty_state or has_ended_card_fields


def check_recent_ended_meeting(
    result=None,
    device_id=None,
    backup_dir=None,
) -> bool:
    """Pass only when the current UI is the historical meetings page."""

    del result
    if backup_dir is None:
        backup_dir = default_backup_dir("tencentmeeting_eval_1")

    ui_text = current_ui_text(device_id, backup_dir)
    if not ui_text:
        logging.error("Unable to read current UI state.")
        return False

    has_history_title = contains_text(ui_text, HISTORY_TITLES)
    has_history_content = _has_history_page_evidence(ui_text)
    has_home_context = contains_text(ui_text, HOME_PAGE_MARKERS)

    if not has_history_title:
        logging.error("Current UI does not show the historical meetings title.")
    if not has_history_content:
        if has_home_context:
            logging.error("Current UI only shows the home-page Historical Meetings entry, not the history page.")
        else:
            logging.error("Current UI does not show a history list, search box, or empty history state.")
    return has_history_title and has_history_content


if __name__ == "__main__":
    print(check_recent_ended_meeting())
