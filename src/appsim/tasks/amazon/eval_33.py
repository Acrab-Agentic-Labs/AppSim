import json
import os
import subprocess

TASK33_ANSWER_SCHEMA = {
    "type": "object",
    "description": "Extract the number of customer service responses received.",
    "properties": {
        "count": {
            "type": "integer",
            "description": "The total number of customer service responses, excluding the initial greeting.",
        }
    },
    "required": ["count"],
    "additionalProperties": False,
}


def verify_customer_service_response_count(result=None, device_id=None, backup_dir=None):
    """Validate task 33: Send messages to customer service and count responses."""
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    if extracted_answer.get("count") != 3:
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
    result = verify_customer_service_response_count()
    print(result)
