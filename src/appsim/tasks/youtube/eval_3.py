from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"
TARGET_ITEM_ID = "all-build-itx-too-late"


def validate_task_three(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    has_search = False
    has_like = False

    for event in reversed(events):
        extra_data = event.get("extra_data", {})
        if event.get("action") == "search_query" and extra_data.get("query") == "itx":
            has_search = True
        if event.get("action") == "toggle_video_like" and extra_data.get("item_id") == TARGET_ITEM_ID and extra_data.get("enabled") == "true":
            has_like = True

    return has_search and has_like


if __name__ == "__main__":
    print(validate_task_three())
