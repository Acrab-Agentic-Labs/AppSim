# Task 12: Change my personal status to Busy.
import json
import os
import subprocess


def validate_task_twelve(result=None, device_id=None, backup_dir=None):
    """Verify task 12: user_001 in accounts.json has about set to Busy."""
    file_path = os.path.join(backup_dir, "accounts.json") if backup_dir else "accounts.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/accounts.json"])
    subprocess.run(cmd, stdout=open(file_path, "w"))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
    except:
        return False

    for item in items:
        if isinstance(item, dict) and item.get("id") == "user_001":
            if item.get("about") == "Busy":
                return True

    return False


if __name__ == "__main__":
    result = validate_task_twelve()
    print(result)
