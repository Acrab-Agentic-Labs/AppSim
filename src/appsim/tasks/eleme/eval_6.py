def validate_addresses_page(result=None, device_id=None):
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

    # if data.get('action') != 'enter_addresses_page':
    #     return False
    # # 【关键】必须进入地址页面
    # if data.get('page') != 'addresses':
    #     return False
    # if result is None:
    #     return False

    # 检测 result 中的final_message是否包含"5个"、"5条"、"5项"、"五个"、"五条"、"五项"中的任意一个
    if "final_message" in result and (
        "5个" in result["final_message"]
        or "5条" in result["final_message"]
        or "5项" in result["final_message"]
        or "五个" in result["final_message"]
        or "五条" in result["final_message"]
        or "五项" in result["final_message"]
    ):
        return True
    else:
        return False


if __name__ == "__main__":
    result = validate_addresses_page()
    print(result)
