from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_APPLY_FILTER = "apply_filter"
ACTION_COMPLETE_ORDER = "complete_order"
PAGE_TAKEOUT = "takeout"
PAGE_CHECKOUT = "checkout"
DELIVERY_DATE_TOMORROW = "明日"
NOON_HOUR_MIN = 11
NOON_HOUR_MAX = 13
NAME_YUXIAO = "于骁"
NAME_YUWEI = "余味"

def validate_task_twenty_two(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    if not all_data:
        return False

    filtered_food_safety = False
    filtered_cross_day = False
    for r in all_data:
        if r.get('action') == ACTION_APPLY_FILTER and r.get('page') == PAGE_TAKEOUT:
            filters = str(r.get('extra_data', {}).get('filters', []))
            if 'FOOD_SAFETY' in filters or 'food_safety' in filters or '食无忧' in filters:
                filtered_food_safety = True
            if 'CROSS_DAY_BOOKING' in filters or 'cross_day_booking' in filters or '跨天预订' in filters:
                filtered_cross_day = True

    if not filtered_food_safety or not filtered_cross_day:
        return False

    order_addresses = []
    for r in all_data:
        if r.get('action') == ACTION_COMPLETE_ORDER and r.get('page') == PAGE_CHECKOUT:
            extra_data = r.get('extra_data', {})
            if not (extra_data.get('delivery_date') and DELIVERY_DATE_TOMORROW in extra_data.get('delivery_date')):
                continue
            delivery_time_slot = extra_data.get('delivery_time_slot')
            if not delivery_time_slot:
                return False
            try:
                hour = int(delivery_time_slot.split('-')[0].split(':')[0])
                if hour < NOON_HOUR_MIN or hour >= NOON_HOUR_MAX:
                    return False
            except:
                return False
            address_name = extra_data.get('delivery_address_name', '')
            if address_name:
                order_addresses.append(address_name)

    has_yuxiao = any(NAME_YUXIAO in addr for addr in order_addresses)
    has_yuwei = any(NAME_YUWEI in addr for addr in order_addresses)
    if not has_yuxiao or not has_yuwei or len(order_addresses) < 2:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_twenty_two()
    print(result)