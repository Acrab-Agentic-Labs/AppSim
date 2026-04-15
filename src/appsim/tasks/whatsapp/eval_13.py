# Task 13: Post a status on the Updates page with a yellow background and the content "Sunshine".
import json
import os
import subprocess


def validate_task_thirteen(result=None, device_id=None, backup_dir=None):
    """Verify task 13: my_status_001 in user_statuses.json has bgColor -415707 and preview Sunshine."""
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

    for item in items:
        if isinstance(item, dict) and item.get("id") == "my_status_001":
            if item.get("bgColor") == -415707 and item.get("preview") == "Sunshine":
                return True

    return False


if __name__ == "__main__":
    result = validate_task_thirteen()
    print(result)
