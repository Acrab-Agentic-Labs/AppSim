# eval_13.py
import json
import os
import subprocess
from io import StringIO


def share_note_check(result=None, device_id=None, backup_dir=None):
    output_buffer = StringIO()
    _USER_ID = "user_current"
    _NOTE_ID = "note_001"

    try:
        # 从设备获取分享记录
        message_file_path = os.path.join(backup_dir, "shares.json") if backup_dir else "shares.json"
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/shares.json"])
        with open(message_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        try:
            with open(message_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        if not data or len(data) == 0:
            return False

        # 查找用户的分享记录
        user_shares = [item for item in data if item.get("userId") == _USER_ID]

        # 如果有最新的分享记录且笔记id是第一篇的id，返回 True
        if user_shares:
            # 按时间排序，获取最新的分享
            latest_share = sorted(user_shares, key=lambda x: x.get("sharedAt", ""), reverse=True)[0]
            shared_note_id = latest_share.get("noteId", "Unknown")
            if shared_note_id == _NOTE_ID:
                return True
            else:
                return False

        return False

    finally:
        # 释放缓冲区资源
        output_buffer.close()


if __name__ == "__main__":
    print(share_note_check())