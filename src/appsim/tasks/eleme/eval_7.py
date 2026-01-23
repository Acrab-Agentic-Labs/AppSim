from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_CANCEL_ORDER = "cancel_order"
PAGE_ORDER = "order"
ORDER_STATUS_VALUE = "待接单"

def validate_task_seven(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        data = all_data[-1] if isinstance(all_data, list) and all_data else all_data
    except:
        return False

    if data.get('action') != ACTION_CANCEL_ORDER or data.get('page') != PAGE_ORDER:
        return False
    extra_data = data.get('extra_data', {})
    if extra_data.get('order_status') != ORDER_STATUS_VALUE or not extra_data.get('cancel_reason') or not extra_data.get('show_dialog', True):
        return False
    return True

if __name__ == '__main__':
    result = validate_task_seven()
    print(result)
