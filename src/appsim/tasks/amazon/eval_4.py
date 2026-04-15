# Task 4: send 'Hello' to customer service.

import json
import os
import subprocess


def validate_task_four(result=None, device_id=None, backup_dir=None):
    """Validate task 4: send 'Hello' to customer service."""
    chat_messages_file_path = os.path.join(backup_dir, "chat_messages.json") if backup_dir else "chat_messages.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/chat_messages.json"])
    subprocess.run(cmd, stdout=open(chat_messages_file_path, "w"))

    try:
        with open(chat_messages_file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except:
        return False

    if not isinstance(messages, list):
        return False

    for message in messages:
        if (message.get("role") == "USER" and
                message.get("content", "").lower() == "hello"):
            return True

    return False


if __name__ == "__main__":
    result = validate_task_four()
    print(result)
