from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_VALUE = "confirm_payment"
PAGE_VALUE = "payment"
MERCHANT_NAME = "McDonald's"
REQUIRED_ITEMS = {"Hash Browns", "Double Cheeseburger"}


def validate_task_eight(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    for event in reversed(events):
        if event.get("action") != ACTION_VALUE or event.get("page") != PAGE_VALUE:
            continue
        extra_data = event.get("extra_data", {})
        item_names = set(extra_data.get("item_names", []))
        if (
            extra_data.get("merchant_name") == MERCHANT_NAME
            and REQUIRED_ITEMS.issubset(item_names)
            and extra_data.get("delivery_mode") == "Schedule"
            and extra_data.get("scheduled_for") == "Tomorrow 12:00 PM"
        ):
            return True
    return False


if __name__ == "__main__":
    print(validate_task_eight())
