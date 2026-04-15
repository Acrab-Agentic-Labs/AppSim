from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_VALUE = "open_page"
PAGE_VALUE = "history"


def validate_task_one(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    for event in reversed(events):
        if event.get("action") == ACTION_VALUE and event.get("page") == PAGE_VALUE:
            return True
    return False


if __name__ == "__main__":
    print(validate_task_one())
