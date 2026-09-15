import json
import os
import subprocess

TASK28_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取用户的小红书号。",
    "properties": {
        "user_num": {
            "type": "string",
            "description": "用户的小红书号。",
        }
    },
    "required": ["user_num"],
    "additionalProperties": False,
}


def verify_account_identifier_retrieved(result=None, device_id=None, backup_dir=None):
    _USER_ID = "user_001"

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    user_num_answer = extracted_answer.get("user_num")
    if user_num_answer is None:
        return False

    message_file_path = os.path.join(backup_dir, "users.json") if backup_dir is not None else "users.json"

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/users.json"])
        with open(message_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not data or len(data) == 0:
        return False

    for u in data:
        if u.get("id") == _USER_ID:
            if str(user_num_answer) == str(u.get("userNum")):
                return True

    return False


if __name__ == "__main__":
    result = verify_account_identifier_retrieved()
    print(result)
