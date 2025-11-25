# 1、发信息给何凯，说“何老师，请明天早上10点来1118会议室开会”
def task1_friend_message_send_check(
    result=None,
    device_id=None,
    backup_dir=None
):
    import os
    import json
    import subprocess

    _RECEIVER_ID="user_9_12",
    _SENDER_ID="current_user",
    _MESSAGE_CONTENT="何老师，请明天早上10点来1118会议室开会",

    message_file_path = os.path.join(backup_dir, 'messages.json') if backup_dir else 'messages.json'

    try:
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
        item = data["privateChatMessages"][_RECEIVER_ID][-1]
        if item["senderId"] == _SENDER_ID and item["content"] == _MESSAGE_CONTENT:
            return True
        else:
            return False
    except:
        return False


if __name__ == "__main__":
    print(task1_friend_message_send_check())
