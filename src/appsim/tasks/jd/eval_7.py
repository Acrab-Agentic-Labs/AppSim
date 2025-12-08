import json
import os
import subprocess


def validate_task_seven(result=None, device_id=None, backup_dir=None):
    """验证任务七：给Apple官方旗舰店发消息问手机什么时候发货"""
    new_messages_file_path = os.path.join(backup_dir, "new_messages.json") if backup_dir else "new_messages.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/new_messages.json"])
    subprocess.run(cmd, stdout=open(new_messages_file_path, "w"))

    try:
        with open(new_messages_file_path, "r", encoding="utf-8") as f:
            new_messages = json.load(f)
    except:
        return False

    # 检查是否有用户发送的新消息"什么时候发货？"
    if not isinstance(new_messages, list):
        return False

    for message in new_messages:
        if (message.get("sender") == "USER" and
                message.get("type") == "TEXT" and
                "什么时候发货" in message.get("content", "")):
            return True

    return False


if __name__ == "__main__":
    result = validate_task_seven()
    print(result)
