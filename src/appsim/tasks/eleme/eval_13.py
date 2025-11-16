import subprocess
import json


def validate_close_notification(result=None, device_id=None):
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

    # 从数组中找到最后一个change_setting操作，且setting_type为系统消息通知的记录
    data = None
    for record in reversed(all_data):
        if record.get("action") == "change_setting":
            extra_data = record.get("extra_data", {})
            if extra_data.get("setting_type") == "系统消息通知":
                data = record
                break

    if data is None:
        return False

    # 检测1: 验证action
    if data.get("action") != "change_setting":
        return False

    # 检测2: 验证page
    if data.get("page") != "settings":
        return False

    # 检测3: 验证timestamp
    if "timestamp" not in data or not isinstance(data["timestamp"], (int, float)):
        return False

    # 检测4: 验证extra_data
    if "extra_data" not in data:
        return False

    extra_data = data["extra_data"]

    # 检测5: 验证设置类型
    if extra_data.get("setting_type") != "系统消息通知":
        return False

    # 检测6: 验证已关闭
    if extra_data.get("enabled", True):
        return False

    # 检测7: 验证显示了关闭成功弹窗
    if not extra_data.get("show_dialog", False):
        return False

    return True


if __name__ == "__main__":
    # 运行验证并输出结果
    result = validate_close_notification()
    print(result)
