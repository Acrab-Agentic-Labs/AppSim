from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_CART_CHECKOUT_SUCCESS = "cart_checkout_success"
PAGE_CART = "cart"

def validate_task_nine(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        data = all_data[-1] if isinstance(all_data, list) and all_data else all_data
    except:
        return False

    if data.get('action') != ACTION_CART_CHECKOUT_SUCCESS or data.get('page') != PAGE_CART:
        return False
    extra_data = data.get('extra_data', {})
    if not extra_data.get('select_all', False) or not extra_data.get('entered_checkout', False) or not extra_data.get('payment_success', False):
        return False
    return True

if __name__ == '__main__':
    result = validate_task_nine()
    print(result)
