from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ADD_ADDRESS = "add_address"
PAGE_ADDRESS = "address"
ADDRESS_KEYWORD = "华中师范大学元宝山学生公寓二期"
NAME_VALUE = "于骁"
PHONE_VALUE = "13022222222"
TAG_VALUE = "学校"
DETAIL_ADDRESS_KEYWORD = "613"

def validate_task_fifteen(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
    except:
        return False

    add_record = next((r for r in reversed(all_data) if r.get('action') == ACTION_ADD_ADDRESS), None)
    if add_record is None or add_record.get('page') != PAGE_ADDRESS:
        return False

    extra_data = add_record.get('extra_data', {})
    if ADDRESS_KEYWORD not in extra_data.get('address', '') or extra_data.get('name') != NAME_VALUE or extra_data.get('phone') != PHONE_VALUE or extra_data.get('tag') != TAG_VALUE or DETAIL_ADDRESS_KEYWORD not in extra_data.get('detail_address', ''):
        return False

    return True

if __name__ == '__main__':
    # 运行验证并输出结果
    result = validate_task_fifteen()
    print(result)
