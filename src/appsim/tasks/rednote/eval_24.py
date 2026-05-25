# eval_24.py
import json
import os
import subprocess

TASK24_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取私信的数目。",
    "properties": {
        "message_count": {
            "type": "integer",
            "description": "私信数目，必须是阿拉伯数字整数。",
        }
    },
    "required": ["message_count"],
    "additionalProperties": False,
}


def eval_24(result=None, device_id=None, backup_dir=None):
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

    return extracted_answer.get("message_count") == len(data)


if __name__ == "__main__":
    result = eval_24()
    print(result)
