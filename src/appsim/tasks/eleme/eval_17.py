from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_COMPLETE_ORDER = "complete_order"
ACTION_SELECT_SORT_OPTION = "select_sort_option"
PAGE_CHECKOUT = "checkout"
PAGE_TAKEOUT = "takeout"
FROM_PAGE_VALUE = "takeout"
SORT_OPTION_VALUE = "距离优先"

def validate_task_seventeen(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    order_record = next((r for r in reversed(all_data) if r.get('action') == ACTION_COMPLETE_ORDER), None)
    if order_record is None or order_record.get('page') != PAGE_CHECKOUT:
        return False

    extra_data = order_record.get('extra_data', {})
    if extra_data.get('from_page') != FROM_PAGE_VALUE or not extra_data.get('payment_success', False):
        return False

    sort_record = next((r for r in reversed(all_data) if r.get('action') == ACTION_SELECT_SORT_OPTION), None)
    if sort_record is None or sort_record.get('page') != PAGE_TAKEOUT:
        return False
    if sort_record.get('extra_data', {}).get('sort_option') != SORT_OPTION_VALUE:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_seventeen()
    print(result)
