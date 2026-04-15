from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_VALUE = "confirm_payment"
PAGE_VALUE = "payment"
SCHEDULED_FOR = "Tomorrow 12:00 PM"
REQUIRED_ITEMS = {
    ("HAWA SMOOTHIES", "Mango Pineapple Smoothie"),
    ("7-Eleven", "Turkey Sandwich"),
}


def validate_task_twenty_three(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    matched_items = set()
    for event in reversed(events):
        if event.get("action") != ACTION_VALUE or event.get("page") != PAGE_VALUE:
            continue

        extra_data = event.get("extra_data", {})
        if extra_data.get("scheduled_for") != SCHEDULED_FOR:
            continue

        merchant_name = str(extra_data.get("merchant_name", "")).strip()
        item_names = extra_data.get("item_names", [])
        if not isinstance(item_names, list):
            continue

        for item_name in item_names:
            pair = (merchant_name, str(item_name).strip())
            if pair in REQUIRED_ITEMS:
                matched_items.add(pair)
        if matched_items.issuperset(REQUIRED_ITEMS):
            return True

    return False


if __name__ == "__main__":
    print(validate_task_twenty_three())
