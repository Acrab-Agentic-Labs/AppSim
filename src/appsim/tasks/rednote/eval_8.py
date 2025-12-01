# eval_8.py
import json
import os
import subprocess


def dislike_note_check(result=None, device_id=None, backup_dir=None):
    _USER_ID = "user_current"
    _NOTE_ID = "note_002"

    # 从设备获取不喜欢记录
    message_file_path = os.path.join(backup_dir, "dislikes.json") if backup_dir is not None else "dislikes.json"
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/dislikes.json"])

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

    # 查找用户的不喜欢记录
    user_dislikes = [item for item in data if item.get("userId") == _USER_ID and item.get("noteId")== _NOTE_ID]

    # 检查是否有最新的不喜欢记录
    if user_dislikes:
        return True

    return False


if __name__ == "__main__":
    print(dislike_note_check())