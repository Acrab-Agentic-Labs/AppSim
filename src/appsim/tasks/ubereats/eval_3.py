from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_VALUE = "save_place"
PAGE_VALUE = "settings_home_set"


def validate_task_three(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    for event in reversed(events):
        if event.get("action") != ACTION_VALUE or event.get("page") != PAGE_VALUE:
            continue
        extra_data = event.get("extra_data", {})
        location = str(extra_data.get("location", "")).strip().lower()
        if extra_data.get("building_type") == "House" and location == "jianghanlu":
            return True
    return False


if __name__ == "__main__":
    print(validate_task_three())
