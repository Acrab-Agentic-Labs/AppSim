from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"
TARGET_ITEM_IDS = {"apple-macbook-neo", "all-macbook-neo"}


def validate_task_two(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    has_search = False
    has_like = False
    has_save = False

    for event in reversed(events):
        extra_data = event.get("extra_data", {})
        if event.get("action") == "search_query" and extra_data.get("query") == "apple":
            has_search = True
        if event.get("action") == "toggle_video_like" and extra_data.get("item_id") in TARGET_ITEM_IDS and extra_data.get("enabled") == "true":
            has_like = True
        if event.get("action") == "toggle_video_save" and extra_data.get("item_id") in TARGET_ITEM_IDS and extra_data.get("enabled") == "true":
            has_save = True

    return has_search and has_like and has_save


if __name__ == "__main__":
    print(validate_task_two())
