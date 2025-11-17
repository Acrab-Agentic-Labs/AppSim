# 6、看看微信好友“同事”发给我的最新消息，阅读他交代我的事情，按他说的做。


def Task6_MessageSendCheck(result=None, device_id=None):
    import json
    import subprocess

    def _MessageSendCheck(receiverId, senderId, message_content, device_id):
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

    ALL_USER = ["user_9_10", "user_9_11"]
    MESSAGE = "明天晚上6点在江汉路小酒馆见面"
    senderId = "current_user"

    try:
        return _MessageSendCheck(
            receiverId=ALL_USER[0], senderId=senderId, message_content=MESSAGE, device_id=device_id
        ) and _MessageSendCheck(receiverId=ALL_USER[1], senderId=senderId, message_content=MESSAGE, device_id=device_id)
    except:
        return False


if __name__ == "__main__":
    print(Task6_MessageSendCheck())
