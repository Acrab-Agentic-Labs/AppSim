import json
import os
import subprocess


def message_send_check(
     result=None, device_id=None,backup_dir=None
):
    # 从设备获取文件内容，直接读取到内存
    # run-as com.example.test05是APP名字；files/messages.json是文件路径
    _RECEIVEER_ID = "user_001"
    _SENDER_ID = "user_current"
    _MESSAGE_CONTENT= "你好"

    message_file_path=os.path.join(backup_dir,"messages.json") if backup_dir is not None else "messages.json"

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.test05", "cat", "files/messages.json"])
        with open(message_file_path,"w") as f:
            subprocess.run(cmd,stdout=f)

        with open(message_file_path, "r",encoding="utf-8") as f:
            data=json.load(f)

        if not data or len(data) == 0:
            return False

        # 获取最新的消息（列表最后一条）
        latest_message = data[-1]

        # 获取sender和receiver的id
        _SENDER_ID = latest_message.get("sender", {}).get("id")
        receiver_id = latest_message.get("receiver", {}).get("id")

        # 检查最新消息是否匹配
        if (
            _SENDER_ID == _SENDER_ID
            and receiver_id == _RECEIVEER_ID
            and latest_message.get("content") == _MESSAGE_CONTENT
            and latest_message.get("type") == "TEXT"
        ):
            return True
        return False
    except:
        return False


if __name__ == "__main__":
    print(message_send_check())
