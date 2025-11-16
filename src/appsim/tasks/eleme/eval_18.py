import subprocess
import json


def validate_contact_merchant(result=None, device_id=None):
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
        all_data = []

    # 从数组中找到最后一个发送消息的记录
    message_record = None
    for record in reversed(all_data):
        if record.get("action") == "send_message":
            message_record = record
            break

    # 检测1: 验证发送消息操作存在
    if message_record is None:
        return False

    # 检测2: 验证page
    if message_record.get("page") != "chat":
        return False

    # 检测3: 验证extra_data存在
    if "extra_data" not in message_record:
        return False

    extra_data = message_record["extra_data"]

    # 检测4: 【关键】验证收件人类型是商家(不能是骑手)
    if extra_data.get("recipient_type") != "merchant":
        return False

    # 检测5: 【关键】验证发送了正确的消息
    if extra_data.get("message") != "缺少可乐，要求退款":
        return False

    return True


if __name__ == "__main__":
    # 运行验证并输出结果
    result = validate_contact_merchant()
    print(result)
