from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
DEVICE_FILE_PATH = "files/messages.json"
ORDER_ACTION = "confirm_payment"
ORDER_PAGE = "payment"
RIDE_ACTION = "request_ride"
RIDE_PAGE = "choose_ride"
REQUIRED_ITEMS = {
    ("Benvenuto Cafe", "Espresso"),
    ("Yunnan Rice Noodle", "Cold Noodle Salad"),
}


def validate_task_thirty_three(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    matched_items = set()
    ride_completed = False

    for event in reversed(events):
        action = event.get("action")
        page = event.get("page")
        extra_data = event.get("extra_data", {})

        if action == ORDER_ACTION and page == ORDER_PAGE:
            merchant_name = str(extra_data.get("merchant_name", "")).strip()
            item_names = extra_data.get("item_names", [])
            if isinstance(item_names, list):
                for item_name in item_names:
                    pair = (merchant_name, str(item_name).strip())
                    if pair in REQUIRED_ITEMS:
                        matched_items.add(pair)

        if action == RIDE_ACTION and page == RIDE_PAGE:
            pickup = str(extra_data.get("pickup_location", "")).strip().lower()
            dropoff = str(extra_data.get("dropoff_location", "")).strip().lower()
            if pickup == "jiedaokou" and dropoff == "jianghanlu":
                ride_completed = True

        if ride_completed and matched_items.issuperset(REQUIRED_ITEMS):
            return True

    return False


if __name__ == "__main__":
    print(validate_task_thirty_three())
