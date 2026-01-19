from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_ORDERS_PAGE = "enter_orders_page"
ACTION_NAVIGATE = "navigate"
PAGE_ORDERS = "orders"
PAGE_MY_ORDERS = "my_orders"
PAGE_ORDER_DETAIL = "order_detail"
ORDER_STATUS_DELIVERED = "已送达"

def validate_task_twenty_three(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    if not all_data:
        return False

    enter_orders_page = any(
        (r.get('action') == ACTION_ENTER_ORDERS_PAGE and r.get('page') == PAGE_ORDERS) or
        (r.get('action') == ACTION_NAVIGATE and r.get('page') == PAGE_MY_ORDERS)
        for r in all_data
        if (r.get('extra_data', {}).get('selected_tab') or r.get('extra_data', {}).get('tab', '全部')) in ['全部', 'all', 'ALL']
    )
    if not enter_orders_page:
        return False

    clicked_first_delivered_order = any(
        r.get('action') == ACTION_NAVIGATE and
        r.get('page') == PAGE_ORDER_DETAIL and
        r.get('extra_data', {}).get('from_page', '') == PAGE_MY_ORDERS and
        (r.get('extra_data', {}).get('order_index', -1) == 2 or r.get('extra_data', {}).get('is_first_order', False)) and
        r.get('extra_data', {}).get('order_status', '') == ORDER_STATUS_DELIVERED
        for r in all_data
    )
    if not clicked_first_delivered_order:
        return False

    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str) or '33' not in final_message:
        return False

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_twenty_three()
    print(result)
