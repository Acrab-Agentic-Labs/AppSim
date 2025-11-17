import json
import subprocess


def validate_search_and_filter(result=None, device_id=None):
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.myele", "cat", "files/messages.json"])
    subprocess.run(cmd, stdout=open("messages.json", "w"))

    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                data = data[-1] if data else {}
    except:
        return False

    if data.get("action") != "filter":
        return False
    if data.get("page") != "search_result":
        return False
    if "extra_data" not in data:
        return False
    extra_data = data["extra_data"]
    # 【关键】搜索关键词必须是"烤鸡"
    if extra_data.get("keyword") != "烤鸡":
        return False
    # 【关键】价格区间必须是0-30
    if extra_data.get("price_min") != 0:
        return False
    if extra_data.get("price_max") != 30:
        return False
    return True


if __name__ == "__main__":
    result = validate_search_and_filter()
    print(result)
