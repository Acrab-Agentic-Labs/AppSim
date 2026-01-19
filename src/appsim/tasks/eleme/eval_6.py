from appsim.utils import read_json_from_device

PACKAGE_NAME = "com.example.myele"
DEVICE_FILE_PATH = "files/messages.json"
ACTION_FILTER = "filter"
PAGE_SEARCH_RESULT = "search_result"
EXTRA_DATA_KEY = "extra_data"
KEYWORD_KEY = "keyword"
KEYWORD_VALUE = "烤鸡"
PRICE_MIN_KEY = "price_min"
PRICE_MIN_VALUE = 0
PRICE_MAX_KEY = "price_max"
PRICE_MAX_VALUE = 30

def validate_task_six(result=None,device_id=None,backup_dir=None):
    try:
        all_data = read_json_from_device(device_id, PACKAGE_NAME, DEVICE_FILE_PATH, backup_dir)
        if isinstance(all_data, list):
            data = all_data[-1] if all_data else {}
        else:
            data = all_data
    except:
        return False

    if data.get('action') != ACTION_FILTER:
        return False
    if data.get('page') != PAGE_SEARCH_RESULT:
        return False
    if EXTRA_DATA_KEY not in data:
        return False
    extra_data = data[EXTRA_DATA_KEY]
    # 【关键】搜索关键词必须是"烤鸡"
    if extra_data.get(KEYWORD_KEY) != KEYWORD_VALUE:
        return False
    # 【关键】价格区间必须是0-30
    if extra_data.get(PRICE_MIN_KEY) != PRICE_MIN_VALUE:
        return False
    if extra_data.get(PRICE_MAX_KEY) != PRICE_MAX_VALUE:
        return False
    return True

if __name__ == '__main__':
    result = validate_task_six()
    print(result)
