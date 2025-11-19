import json
import subprocess


# 验证任务26: 点击搜索框,在搜索历史页面找到"清除历史"按钮并点击
# 关键验证点:
# 1. 必须进入搜索页面(search页面)
# 2. 必须点击删除历史记录按钮
def validate_clear_search_history(result=None, device_id=None):
    # 从设备获取文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.myele", "cat", "files/messages.json"])
    subprocess.run(cmd, stdout=open("messages.json", "w"))

    # 读取文件
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except:
        return False

    # 检查是否有数据
    if not all_data:
        return False

    # 检测1: 验证进入搜索页面
    entered_search = False
    for record in all_data:
        if record.get("action") == "navigate" and record.get("page") == "search":
            entered_search = True
            break

    if not entered_search:
        return False

    # 检测2: 验证点击清除历史记录按钮
    clicked_clear_history = False
    for record in all_data:
        if record.get("action") == "clear_search_history" and record.get("page") == "search":
            clicked_clear_history = True
            break

    if not clicked_clear_history:
        return False

    return True


if __name__ == "__main__":
    # 运行验证并输出结果
    result = validate_clear_search_history()
    print(result)
