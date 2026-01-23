from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_SEND_MESSAGE = "send_message"
PAGE_CHAT = "chat"
RECIPIENT_TYPE_MERCHANT = "merchant"
MESSAGE_VALUE = "缺少可乐，要求退款"

def validate_task_sixteen(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    message_record = next((r for r in reversed(all_data or []) if r.get('action') == ACTION_SEND_MESSAGE), None)
    if message_record is None or message_record.get('page') != PAGE_CHAT:
        return False

    extra_data = message_record.get('extra_data', {})
    if extra_data.get('recipient_type') != RECIPIENT_TYPE_MERCHANT or extra_data.get('message') != MESSAGE_VALUE:
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_sixteen()
    print(result)
