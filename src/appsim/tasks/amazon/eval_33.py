import json
import os
import subprocess


def validate_task_thirty_three(result=None, device_id=None, backup_dir=None):
    """Validate task 33: Send 'Hi', 'I have a question about my order', and 'I want to cancel' to the customer service one by one. Let me know how many customer service responses you have received in total, excluding the initial greeting message from the customer service. Please return the number in Arabic numerals only."""
    # Check final_message contains "3"
    message_answer_ok = False
    if result and "final_message" in result and result["final_message"] is not None:
        if "3" in result["final_message"]:
            message_answer_ok = True

    if not message_answer_ok:
        return False

    # Check chat_messages.json has the 3 user messages with exact content
    chat_messages_file_path = os.path.join(backup_dir, "chat_messages.json") if backup_dir else "chat_messages.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/chat_messages.json"])
    subprocess.run(cmd, stdout=open(chat_messages_file_path, "w"))

    try:
        with open(chat_messages_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            messages = data if isinstance(data, list) else []
    except:
        return False

    expected_user_messages = ["Hi", "I have a question about my order", "I want to cancel"]
    user_messages = [
        msg.get("content", "")
        for msg in messages
        if isinstance(msg, dict) and msg.get("sender") == "USER"
    ]

    for expected in expected_user_messages:
        if expected not in user_messages:
            return False

    return True


if __name__ == "__main__":
    result = validate_task_thirty_three()
    print(result)
