from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_ORDERS_PAGE = "enter_orders_page"
PAGE_ORDERS = "orders"
EXTRA_DATA_KEY = "extra_data"
EXTRA_DATA_SELECTED_TAB_KEY = "selected_tab"
EXTRA_DATA_SELECTED_TAB_VALUE = "全部"

TASK5_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取最近一个订单的状态。",
    "properties": {
        "order_status": {
            "type": "string",
            "description": "订单状态文本，例如待接单、配送中、已送达等。",
        }
    },
    "required": ["order_status"],
    "additionalProperties": False,
}


def validate_task_five(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        if isinstance(all_data, list):
            data = all_data[-1] if all_data else {}
        else:
            data = all_data
    except:
        return False

    if data.get('action') != ACTION_ENTER_ORDERS_PAGE:
        return False
    if data.get('page') != PAGE_ORDERS:
        return False
    if EXTRA_DATA_KEY not in data:
        return False
    extra_data = data[EXTRA_DATA_KEY]
    if extra_data.get(EXTRA_DATA_SELECTED_TAB_KEY) != EXTRA_DATA_SELECTED_TAB_VALUE:
        return False

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    status = str(extracted_answer.get("order_status") or "")
    return "待接单" in status
