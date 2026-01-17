# eval_14.py
import json
import os
import subprocess


def send_message_check(result=None, device_id=None, backup_dir=None):
    # 从设备获取消息记录
    message_file_path = os.path.join(backup_dir, "messages.json") if backup_dir is not None else "messages.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/messages.json"])

    # 将数据写入备份文件
    with open(message_file_path, "w") as f:
        subprocess.run(cmd, stdout=f)

    try:
        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not data or len(data) == 0:
        return False

    # 获取最后一条消息
    last_message = data[-1]

    # 检查 content 和 receiver.id
    content = last_message.get("content", "")
    receiver_id = last_message.get("receiver", {}).get("id", "")

    if content == "催更" and receiver_id == "user_002":
        return True
    else:
        return False


if __name__ == "__main__":
    print(send_message_check())