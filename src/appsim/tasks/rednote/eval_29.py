import json
import os
import subprocess

TASK29_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取关注的博主中最受大众关注的博主名称。",
    "properties": {
        "nickname": {
            "type": "string",
            "description": "最受大众关注的博主昵称。",
        }
    },
    "required": ["nickname"],
    "additionalProperties": False,
}


def eval_29(result=None, device_id=None, backup_dir=None):
    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False

    nickname_answer = extracted_answer.get("nickname")
    if nickname_answer is None:
        return False

    follows_path = os.path.join(backup_dir, "follows.json") if backup_dir else "follows.json"
    users_path = os.path.join(backup_dir, "users.json") if backup_dir else "users.json"

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/follows.json"])
        with open(follows_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/users.json"])
        with open(users_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(follows_path, "r", encoding="utf-8") as f:
            follows = json.load(f)

        with open(users_path, "r", encoding="utf-8") as f:
            users = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not follows or not users:
        return False

    user_ids = set()
    for item in follows:
        if "followerId" in item:
            user_ids.add(item["followerId"])
        if "followingId" in item:
            user_ids.add(item["followingId"])

    candidates = [u for u in users if u.get("id") in user_ids]
    if not candidates:
        return False

    max_user = max(candidates, key=lambda u: u.get("followerCount", 0))
    nickname = max_user.get("nickname")

    return nickname == nickname_answer


if __name__ == "__main__":
    result = eval_29()
    print(result)
