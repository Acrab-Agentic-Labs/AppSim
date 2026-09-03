# 2、发信息到工作群，说“GUI Agent最近很火，我觉得挺有意思的”
import os
import json
import subprocess


def verify_group_message_sent(
    result=None,
    device_id=None,
    backup_dir=None
):
    _GROUP_ID = "group_2"
    _SENDER_ID = "current_user"
    _MESSAGE_CONTENT = "GUI Agent最近很火，我觉得挺有意思的"

    message_file_path = os.path.join(backup_dir, 'messages.json') if backup_dir else 'messages.json'

    try:
        # adb拿到文件
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.fakewechat", "cat", "files/messages.json"])
        with open(message_file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)

        # 打开此文件
        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # 检查聊天记录
        messages = data.get("groupChatMessages", {}).get(_GROUP_ID, [])
        if not messages:
            return False

        item = messages[-1]
        return item.get("senderId") == _SENDER_ID and item.get("content") == _MESSAGE_CONTENT
    except Exception:
        return False


if __name__ == "__main__":
    print(verify_group_message_sent())
