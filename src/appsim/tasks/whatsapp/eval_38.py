# Task 38: React to every friend's status with a purple heart.
import json
import os
import subprocess


def validate_task_thirty_eight(result=None, device_id=None, backup_dir=None):
    """Verify task 38: every item except the first one in user_statuses.json has userReaction set to 💜."""
    file_path = os.path.join(backup_dir, "user_statuses.json") if backup_dir else "user_statuses.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/user_statuses.json"])
    subprocess.run(cmd, stdout=open(file_path, "w"))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
    except:
        return False

    if len(items) < 2:
        return False

    for item in items[1:]:
        if not isinstance(item, dict):
            return False
        if item.get("userReaction") != "💜":
            return False

    return True


if __name__ == "__main__":
    result = validate_task_thirty_eight()
    print(result)
