from appsim.utils import read_json_from_device


PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"
STATE_FILE_PATH = "files/task_state.json"
TARGET_ITEM_ID = "music-blue-porcelain"
TARGET_TEXT = "This MV looks really clear"
QUALITY_PAGES = {"quality", "quality_settings"}
QUALITY_GROUP_KEYS = {"quality_mobile", "quality_wifi"}


def validate_task_thirty_three(result=None, device_id=None, backup_dir=None):
    try:
        message_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        state = read_json_from_device(device_id, PACKAGE_NAME, STATE_FILE_PATH, backup_dir)
        events = message_data if isinstance(message_data, list) else [message_data]
    except Exception:
        return False

    enabled_quality = False
    posted_comment = False

    for event in reversed(events):
        extra_data = event.get("extra_data", {})
        if event.get("action") == "select_option" and event.get("page") in QUALITY_PAGES:
            if (
                extra_data.get("group_key") in QUALITY_GROUP_KEYS
                and extra_data.get("option_key") == "higher_picture_quality"
            ):
                enabled_quality = True
        if event.get("action") == "submit_comment" and event.get("page") == "comments_sheet":
            if extra_data.get("item_id") == TARGET_ITEM_ID and extra_data.get("text") == TARGET_TEXT:
                posted_comment = True

    selected_options = state.get("selected_options", {})
    quality_persisted = any(
        selected_options.get(group_key) == "higher_picture_quality"
        for group_key in QUALITY_GROUP_KEYS
    )
    return enabled_quality and quality_persisted and posted_comment


if __name__ == "__main__":
    print(validate_task_thirty_three())
