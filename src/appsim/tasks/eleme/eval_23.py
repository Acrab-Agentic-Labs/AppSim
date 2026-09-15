from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_ORDERS_PAGE = "enter_orders_page"
ACTION_NAVIGATE = "navigate"
PAGE_ORDERS = "orders"
PAGE_MY_ORDERS = "my_orders"
PAGE_ORDER_DETAIL = "order_detail"
ORDER_STATUS_DELIVERED = "已送达"

TASK23_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取最新已送达订单的实付金额。",
    "properties": {
        "amount": {
            "type": "string",
            "description": "实付金额数值。仅输出数字，不含单位和货币符号。",
        }
    },
    "required": ["amount"],
    "additionalProperties": False,
}


def verify_latest_delivered_order_paid_amount(result=None, device_id=None, backup_dir=None):
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

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    amount = str(extracted_answer.get("amount") or "")
    return "33" in amount
