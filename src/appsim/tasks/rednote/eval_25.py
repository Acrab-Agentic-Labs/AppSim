import json
import os
import subprocess

def eval_25(result=None, device_id=None, backup_dir=None):
    _USER_ID="user_001"

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
            if result == u.get("followerCount")+ u.get("followingCount"):
                return True


if __name__ == "__main__":
    result = eval_25()
    print(result)
