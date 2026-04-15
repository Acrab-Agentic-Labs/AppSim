from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.youtube_sim"
DEVICE_FILE_PATH = "files/messages.json"


def validate_task_seven(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    for event in reversed(events):
        extra_data = event.get("extra_data", {})
        if event.get("action") != "toggle_channel_subscription":
            continue
        if extra_data.get("channel_key") == "jay_chou" and extra_data.get("enabled") == "true":
            return True
    return False


if __name__ == "__main__":
    print(validate_task_seven())
