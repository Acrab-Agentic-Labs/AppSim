from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.ubereats_sim"
DEVICE_FILE_PATH = "files/app_state.json"


def validate_task_four(result=None, device_id=None, backup_dir=None):
    try:
        state = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except Exception:
        return False

    cart_items = state.get("cartItems", [])
    return isinstance(cart_items, list) and len(cart_items) == 0


if __name__ == "__main__":
    print(validate_task_four())
