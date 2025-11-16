# 1、发信息给何凯，说“何老师，请明天早上10点来1118会议室开会”
def Task1_MessageSendCheck(
    receiverId="user_9_12",
    senderId="current_user",
    message_content="何老师，请明天早上10点来1118会议室开会",
    result=None,
    device_id=None,
):
    import subprocess
    import json

    try:
        # adb拿到文件
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.fakewechat", "cat", "files/messages.json"])
        subprocess.run(cmd, stdout=open("messages.json", "w"))

        # 打开此文件
        with open("messages.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        # 检查聊天记录
        item = data["privateChatMessages"][receiverId][-1]
        if item["senderId"] == senderId and item["content"] == message_content:
            return True
        else:
            return False
    except:
        return False


if __name__ == "__main__":
    print(Task1_MessageSendCheck())
