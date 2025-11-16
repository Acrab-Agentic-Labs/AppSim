import subprocess
import json


def validate_sort_selection(result=None, device_id=None):
    # cmd = ['adb']
    # if device_id:
    #     cmd.extend(['-s', device_id])
    # cmd.extend(['exec-out', 'run-as', 'com.example.myele', 'cat', 'files/messages.json'])
    # subprocess.run(cmd, stdout=open('messages.json', 'w'))

    # try:
    #     with open('messages.json', 'r', encoding='utf-8') as f:
    #         data = json.load(f)
    #         if isinstance(data, list):
    #             data = data[-1] if data else {}
    # except:
    #     return False

    # if data.get('action') != 'select_sort_option':
    #     return False
    # if data.get('page') != 'takeout':
    #     return False
    # if 'extra_data' not in data:
    #     return False
    # extra_data = data['extra_data']
    # # 【关键】排序选项必须是"好评优先"
    # if extra_data.get('sort_option') != '好评优先':
    #     return False
    # # 【关键】必须点击"综合排序"
    # if extra_data.get('sort_type') != '综合排序':
    #     return False
    # if result is None:
    #     return False

    # 检测 result 中的final_messages中是否包含 "肯德基"
    if "final_message" in result and "肯德基" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    result = validate_sort_selection()
    print(result)
