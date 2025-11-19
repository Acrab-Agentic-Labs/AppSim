import json
import subprocess


def SendMessageCheck(result=None, device_id=None):
    """
    检查最后一条消息是否符合条件：
    - content = "催更"
    - receiver.id = "user_002"
    """
    # 从设备获取消息记录
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["exec-out", "run-as", "com.example.test05", "cat", "files/messages.json"],
    )
    result1 = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # 检查命令是否成功执行
    if result1.returncode != 0 or not result1.stdout:
        print(" Failed to read messages file")
        print(f"   Reason: ADB command failed (return code: {result1.returncode})")
        if result1.stderr:
            print(f"   Error: {result1.stderr}")
        return False

    # 解析 JSON
    try:
        data = json.loads(result1.stdout)
    except:
        print(" Failed to parse messages data")
        print("   Reason: Invalid JSON format")
        return False

    # 检查最后一条消息
    try:
        if not data or len(data) == 0:
            print(" Messages list is empty")
            print("   Reason: No message records found")
            print("   Expected: At least one message with content='催更' and receiver.id='user_002'")
            return False

        # 获取最后一条消息
        last_message = data[-1]

        # 检查 content 和 receiver.id
        content = last_message.get("content", "")
        receiver_id = last_message.get("receiver", {}).get("id", "")

        if content == "催更" and receiver_id == "user_002":
            print("✓ Successfully sent message")
            print(f"   Content: {content}")
            print(f"   Receiver ID: {receiver_id}")
            print(f"   Receiver Name: {last_message.get('receiver', {}).get('nickname', 'Unknown')}")
            print(f"   Sent at: {last_message.get('createdAt', 'Unknown')}")
            return True
        else:
            print(" Last message does not match requirements")
            print("   Expected: content='催更' and receiver.id='user_002'")
            print(f"   Actual: content='{content}' and receiver.id='{receiver_id}'")
            if receiver_id == "user_002":
                print("   Note: Receiver is correct, but content is wrong")
            elif content == "催更":
                print("   Note: Content is correct, but receiver is wrong")
            return False

    except:
        print(" Error while checking message records")
        return False


if __name__ == "__main__":
    print(SendMessageCheck())
