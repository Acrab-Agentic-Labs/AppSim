from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_APPLY_FILTER = "apply_filter"
ACTION_COMPLETE_ORDER = "complete_order"
PAGE_TAKEOUT = "takeout"
PAGE_CHECKOUT = "checkout"
FILTER_CROSS_DAY = "跨天预订"
DELIVERY_TYPE_SCHEDULED = "scheduled"
DELIVERY_DATE_TOMORROW = "明日"
NOON_HOUR_MIN = 11
NOON_HOUR_MAX = 13

def validate_task_eighteen(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    filter_record = next((r for r in reversed(all_data) if r.get('action') == ACTION_APPLY_FILTER), None)
    if filter_record is None or filter_record.get('page') != PAGE_TAKEOUT:
        return False
    if FILTER_CROSS_DAY not in filter_record.get('extra_data', {}).get('filters', []):
        return False

    order_record = next((r for r in reversed(all_data) if r.get('action') == ACTION_COMPLETE_ORDER), None)
    if order_record is None or order_record.get('page') != PAGE_CHECKOUT:
        return False

    extra_data = order_record.get('extra_data', {})
    if extra_data.get('from_page') != PAGE_TAKEOUT or not extra_data.get('payment_success', False):
        return False
    if extra_data.get('delivery_type') != DELIVERY_TYPE_SCHEDULED or extra_data.get('delivery_date') != DELIVERY_DATE_TOMORROW:
        return False

    delivery_time_slot = extra_data.get('delivery_time_slot', '')
    if not delivery_time_slot:
        return False
    try:
        hour = int(delivery_time_slot.split('-')[0].split(':')[0])
        if hour < NOON_HOUR_MIN or hour >= NOON_HOUR_MAX:
            return False
    except:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_eighteen()
    print(result)
