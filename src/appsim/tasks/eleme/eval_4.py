from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.eleme_sim"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_ENTER_ADDRESSES_PAGE = "enter_addresses_page"
PAGE_ADDRESSES = "addresses"

def validate_task_four(result=None,device_id=None,backup_dir=None):
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
    # 【关键】必须进入地址页面
    if data.get('page') != PAGE_ADDRESSES:
        return False
    if result is None:
        return False
    final_message = result.get("final_message")
    if not isinstance(final_message, str):
        return False

    # 检测 result 中的final_message是否包含"5个"、"5条"、"5项"、"五个"、"五条"、"五项"中的任意一个
    if 'final_message' in result and (
            "5个" in result['final_message'] or
            "5条" in result['final_message'] or
            "5项" in result['final_message'] or
            "五个" in result['final_message'] or
            "五条" in result['final_message'] or
            "五项" in result['final_message']
    ):
        return True
    else:
        return False

if __name__ == '__main__':
    result = validate_task_four()
    print(result)
