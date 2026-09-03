# 14、从"发现"进入朋友圈，浏览好友朋友圈，找到第一个推荐电影的好友，然后发消息问她："是什么电影呀？可以给我讲一下是什么主题的吗？"
import os
import json
import subprocess


def verify_moment_author_question_sent(result=None, device_id=None, backup_dir=None):
    _RECEIVER_ID = "user_25"
    _SENDER_ID = "current_user"
    _MESSAGE_CONTENT = "是什么电影呀？可以给我讲一下是什么主题的吗？"

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
        item = data["privateChatMessages"][_RECEIVER_ID][-1]
        if item["senderId"] == _SENDER_ID and item["content"] == _MESSAGE_CONTENT:
            return True
        else:
            return False
    except:
        return False


if __name__ == "__main__":
    print(verify_moment_author_question_sent())
