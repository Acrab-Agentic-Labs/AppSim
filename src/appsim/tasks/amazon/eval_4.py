# Task 4: send 'hello, I have some questions about dyson products.' to customer service.

import json
import os
import subprocess


TARGET_MESSAGE = "hello, I have some questions about dyson products."


def verify_customer_service_message_sent(result=None, device_id=None, backup_dir=None):
    """Validate task 4: send 'Hello, I have some questions about Dyson products.' to customer service."""
    chat_messages_file_path = os.path.join(backup_dir, "chat_messages.json") if backup_dir else "chat_messages.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/chat_messages.json"])
    with open(chat_messages_file_path, "w", encoding="utf-8") as output_file:
        subprocess.run(cmd, stdout=output_file)

    try:
        with open(chat_messages_file_path, "r", encoding="utf-8") as f:
            messages = json.load(f)
    except Exception:
        return False

    if not isinstance(messages, list):
        return False

    for message in messages:
        if not isinstance(message, dict):
            continue

        role = str(message.get("role", "")).strip().upper()
        content = str(message.get("content", "")).strip().lower()

        if role == "USER" and content == TARGET_MESSAGE:
            return True

    return False


if __name__ == "__main__":
    result = verify_customer_service_message_sent()
    print(result)
