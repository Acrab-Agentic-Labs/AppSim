import subprocess
import json


def MessageSendCheck(
    receiverId="user_001", senderId="user_current", message_content="你好", result=None, device_id=None
):
    # 从设备获取文件内容，直接读取到内存
    # run-as com.example.test05是APP名字；files/messages.json是文件路径
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/messages.json"])

    result1 = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if result1.returncode != 0 or not result1.stdout:
        return False

    # 直接从命令输出解析 JSON
    try:
        data = json.loads(result1.stdout)
    except:
        return False

    # 只检查最新发送的消息是否匹配
    try:
        # 检查消息列表是否为空
        if not data or len(data) == 0:
            return False

        # 获取最新的消息（列表最后一条）
        latest_message = data[-1]

        # 获取sender和receiver的id
        sender_id = latest_message.get("sender", {}).get("id")
        receiver_id = latest_message.get("receiver", {}).get("id")

        # 检查最新消息是否匹配
        if (
            sender_id == senderId
            and receiver_id == receiverId
            and latest_message.get("content") == message_content
            and latest_message.get("type") == "TEXT"
        ):
            return True
        return False
    except:
        return False


if __name__ == "__main__":
    print(
        MessageSendCheck(
            receiverId="user_001",  # 小红薯美妆达人的id是user_001
            senderId="user_current",  # 这是"我"
            message_content="你好",  # 发送内容
        )
    )
