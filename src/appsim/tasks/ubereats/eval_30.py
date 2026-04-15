from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
MESSAGES_FILE_PATH = "files/messages.json"
APP_STATE_FILE_PATH = "files/app_state.json"
ACTION_VALUE = "send_message"
PAGE_VALUE = "sendmessages"
MESSAGE_VALUE = "How long will it take to arrive?"


def validate_task_thirty(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, MESSAGES_FILE_PATH, backup_dir)
        state = read_json_from_device(device_id, PACKAGE_NAME, APP_STATE_FILE_PATH, backup_dir)
        events = all_data if isinstance(all_data, list) else [all_data]
    except Exception:
        return False

    orders = state.get("orders", [])
    if not orders:
        return False
    latest_order = orders[0]
    latest_order_id = latest_order.get("id")
    latest_merchant = latest_order.get("merchantName")

    for event in reversed(events):
        if event.get("action") != ACTION_VALUE:
            continue
        if event.get("page") != PAGE_VALUE:
            continue

        extra_data = event.get("extra_data", {})
        if (
            str(extra_data.get("message", "")).strip() == MESSAGE_VALUE
            and extra_data.get("order_id") == latest_order_id
            and extra_data.get("merchant_name") == latest_merchant
        ):
            return True

    return False


if __name__ == "__main__":
    print(validate_task_thirty())
