from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_ADDRESSES_PAGE = "enter_addresses_page"
PAGE_ADDRESSES = "addresses"

TASK4_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取保存的地址信息中于骁的信息数量。",
    "properties": {
        "count": {
            "type": "integer",
            "description": "于骁的地址信息数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def validate_task_four(result=None, device_id=None, backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        if isinstance(all_data, list):
            data = all_data[-1] if all_data else {}
        else:
            data = all_data
    except:
        return False

    if data.get('action') != ACTION_ENTER_ADDRESSES_PAGE:
        return False
    if data.get('page') != PAGE_ADDRESSES:
        return False

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    count = extracted_answer.get("count")
    return count == 5
