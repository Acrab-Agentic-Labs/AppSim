from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_VALUE = "open_payment"
PAGE_VALUE = "payment"
MERCHANT_NAME = "McDonald's"
ITEM_NAME = "Hash Browns"


def validate_task_two(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    for event in reversed(events):
        if event.get("action") != ACTION_VALUE or event.get("page") != PAGE_VALUE:
            continue
        extra_data = event.get("extra_data", {})
        item_names = extra_data.get("item_names", [])
        if (
            extra_data.get("merchant_name") == MERCHANT_NAME
            and ITEM_NAME in item_names
            and extra_data.get("total_quantity") == 1
            and extra_data.get("delivery_mode") == "Standard"
            and extra_data.get("scheduled_for") == ""
            and extra_data.get("default_delivery") is True
        ):
            return True
    return False


if __name__ == "__main__":
    print(validate_task_two())
