import json
import subprocess


def validate_cancel_order(result=None, device_id=None):
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

    if data.get("action") != "cancel_order":
        return False
    if data.get("page") != "order":
        return False
    if "extra_data" not in data:
        return False
    extra_data = data["extra_data"]
    # 【关键】订单状态必须是"待接单"
    if extra_data.get("order_status") != "待接单":
        return False
    # 【关键】必须选择取消原因
    if not extra_data.get("cancel_reason"):
        return False
    # 【关键】必须显示弹窗
    if not extra_data.get("show_dialog", True):
        return False
    return True


if __name__ == "__main__":
    result = validate_cancel_order()
    print(result)
