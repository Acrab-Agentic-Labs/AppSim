# 2、发信息到工作群，说“GUI Agent最近很火，我觉得挺有意思的”
def Task2_MessageSendCheck(
    group_id="group_2",
    senderId="current_user",
    message_content="GUI Agent最近很火，我觉得挺有意思的",
    result=None,
    device_id=None,
):
    import json
    import subprocess

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
        item = data["groupChatMessages"][group_id][-1]
        if item["senderId"] == senderId and item["content"] == message_content:
            return True
        else:
            return False
    except:
        return False


if __name__ == "__main__":
    print(Task2_MessageSendCheck())
