from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_COMPLETE_ORDER = "complete_order"
PAGE_CHECKOUT = "checkout"
SEARCH_QUERY_VALUE = "肯德基"

def validate_task_twelve(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    order_record = None
    for record in reversed(all_data):
        if record.get('action') == ACTION_COMPLETE_ORDER:
            order_record = record
            break

    if order_record is None or order_record.get('page') != PAGE_CHECKOUT:
        return False

    extra_data = order_record.get('extra_data', {})
    if extra_data.get('search_query') != SEARCH_QUERY_VALUE or not extra_data.get('added_to_cart', False) or not extra_data.get('used_coupon', False) or not extra_data.get('selected_max_coupon', False) or not extra_data.get('payment_success', False):
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_twelve()
    print(result)
