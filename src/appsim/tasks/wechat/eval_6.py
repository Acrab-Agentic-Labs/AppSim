# 6、看看微信好友“同事”发给我的最新消息，阅读他交代我的事情，按他说的做。
import os
import json
import subprocess

def task6_validate_forward_message(result=None, device_id=None, backup_dir=None):
    def _validate_message_send(receiverId, senderId, message_content, result, device_id, backup_dir):
        try:
            message_file_path = os.path.join(backup_dir, 'messages.json') if backup_dir else 'messages.json'

            # adb拿到文件
            cmd = ["adb"]
            if device_id:
                cmd.extend(["-s", device_id])
            cmd.extend(["exec-out", "run-as", "com.example.fakewechat", "cat", "files/messages.json"])

            with open(message_file_path, "w", encoding="utf-8") as f:
                subprocess.run(cmd, stdout=f)

            # 打开此文件
            with open(message_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # 检查聊天记录
            item = data["privateChatMessages"][receiverId][-1]
            if item["senderId"] == senderId and item["content"] == message_content:
                return True
            else:
                return False
        except:
            return False

    _ALL_USERS = ["user_9_10", "user_9_11"]
    _MESSAGE = "明天晚上6点在江汉路小酒馆见面"
    _SENDER_ID = "current_user"

    try:
        return _validate_message_send(
            receiverId=_ALL_USERS[0], senderId=_SENDER_ID, message_content=_MESSAGE, result=result, device_id=device_id, backup_dir=backup_dir
        ) and _validate_message_send(receiverId=_ALL_USERS[1], senderId=_SENDER_ID, message_content=_MESSAGE, result=result, device_id=device_id, backup_dir=backup_dir)
    except:
        return False


if __name__ == "__main__":
    print(task6_validate_forward_message())
