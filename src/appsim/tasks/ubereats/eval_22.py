from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_VALUE = "add_to_cart"
PAGE_VALUE = "product_detail"
REQUIRED_ITEMS = {
    ("McDonald's", "Hash Browns"),
    ("McDonald's", "Double Cheeseburger"),
    ("Burger King", "Whopper"),
}


def validate_task_twenty_two(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    matched_items = set()
    for event in events:
        if event.get("action") != ACTION_VALUE or event.get("page") != PAGE_VALUE:
            continue

        extra_data = event.get("extra_data", {})
        merchant_name = str(extra_data.get("merchant_name", "")).strip()
        item_name = str(extra_data.get("item_name", "")).strip()
        if (merchant_name, item_name) in REQUIRED_ITEMS:
            matched_items.add((merchant_name, item_name))
        if merchant_name == "McDonald's" and item_name == "Hash Brown":
            matched_items.add(("McDonald's", "Hash Browns"))

    return matched_items.issuperset(REQUIRED_ITEMS)


if __name__ == "__main__":
    print(validate_task_twenty_two())
