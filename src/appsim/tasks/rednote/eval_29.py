import json
import os
import subprocess

def eval_29(result=None, device_id=None, backup_dir=None):
    follows_path = os.path.join(backup_dir, "follows.json") if backup_dir else "follows.json"
    users_path = os.path.join(backup_dir, "users.json") if backup_dir else "users.json"

    try:
        # 拉 follows.json
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/follows.json"])
        with open(follows_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        # 拉 users.json
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/users.json"])
        with open(users_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        # 读取数据
        with open(follows_path, "r", encoding="utf-8") as f:
            follows = json.load(f)

        with open(users_path, "r", encoding="utf-8") as f:
            users = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not follows or not users:
        return False

    # 1. 收集第一个文件中出现的用户 id
    user_ids = set()
    for item in follows:
        if "followerId" in item:
            user_ids.add(item["followerId"])
        if "followingId" in item:
            user_ids.add(item["followingId"])

    # 2. 在 users 中筛选
    candidates = [u for u in users if u.get("id") in user_ids]
    if not candidates:
        return False

    # 3. 找 followerCount 最大的用户
    max_user = max(candidates, key=lambda u: u.get("followerCount", 0))
    nickname = max_user.get("nickname")

    # 4. 校验结果
    return nickname == result


if __name__ == "__main__":
    result = eval_29()
    print(result)
