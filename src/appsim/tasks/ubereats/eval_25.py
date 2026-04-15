from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_VALUE = "toggle_favorite"
PAGE_VALUE = "home"
REQUIRED_FAVORITES = {"McDonald's", "VINEYARD", "Burger King"}


def validate_task_twenty_five(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    favorite_states = {}
    for event in events:
        if event.get("action") != ACTION_VALUE or event.get("page") != PAGE_VALUE:
            continue

        extra_data = event.get("extra_data", {})
        merchant_name = str(extra_data.get("merchant_name", "")).strip()
        if merchant_name not in REQUIRED_FAVORITES:
            continue
        favorite_states[merchant_name] = extra_data.get("favorited") is True

    return all(favorite_states.get(merchant_name) is True for merchant_name in REQUIRED_FAVORITES)


if __name__ == "__main__":
    print(validate_task_twenty_five())
