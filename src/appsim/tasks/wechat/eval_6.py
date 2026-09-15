# 6、看看微信好友“同事”发给我的最新消息，阅读他交代我的事情，按他说的做。
import os
import json
import subprocess


def verify_latest_message_instructions_completed(result=None, device_id=None, backup_dir=None):
    def _validate_message_send(data, receiver_id, sender_id, message_content):
        messages = data.get("privateChatMessages", {}).get(receiver_id, [])
        if not messages:
            return False

        item = messages[-1]
        return item.get("senderId") == sender_id and item.get("content") == message_content

    _ALL_USERS = ["user_9_10", "user_9_11"]
    _MESSAGE = "明天晚上6点在江汉路小酒馆见面"
    _SENDER_ID = "current_user"

    try:
        message_file_path = os.path.join(backup_dir, 'messages.json') if backup_dir else 'messages.json'

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

        return _validate_message_send(
            data=data,
            receiver_id=_ALL_USERS[0],
            sender_id=_SENDER_ID,
            message_content=_MESSAGE,
        ) and _validate_message_send(
            data=data,
            receiver_id=_ALL_USERS[1],
            sender_id=_SENDER_ID,
            message_content=_MESSAGE,
        )
    except Exception:
        return False


if __name__ == "__main__":
    print(verify_latest_message_instructions_completed())
