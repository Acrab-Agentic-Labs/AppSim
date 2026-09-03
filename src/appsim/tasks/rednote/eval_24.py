# eval_24.py
import json
import os
import subprocess

TASK24_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取用户回答中的私信消息总条数。",
    "properties": {
        "message_count": {
            "type": "integer",
            "description": "私信消息总条数，必须是阿拉伯数字整数；注意不是私信会话数量，而是所有私信消息的总数。",
        }
    },
    "required": ["message_count"],
    "additionalProperties": False,
}


def verify_private_message_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    message_file_path = os.path.join(backup_dir, "messages.json") if backup_dir is not None else "messages.json"

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/messages.json"])
        with open(message_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not data or len(data) == 0:
        return False

    expected_message_count = len(data)
    return extracted_answer.get("message_count") == expected_message_count


if __name__ == "__main__":
    result = verify_private_message_count()
    print(result)
