# eval_25.py
import json
import os
import subprocess

TASK25_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取关注和粉丝的总人数。",
    "properties": {
        "total_count": {
            "type": "integer",
            "description": "关注人数与粉丝人数之和，必须是阿拉伯数字整数。",
        }
    },
    "required": ["total_count"],
    "additionalProperties": False,
}


def verify_following_and_follower_count(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    _USER_ID = "user_001"
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
            expected = u.get("followerCount", 0) + u.get("followingCount", 0)
            return extracted_answer.get("total_count") == expected

    return False


if __name__ == "__main__":
    result = verify_following_and_follower_count()
    print(result)
