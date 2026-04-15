# Task 7: Follow the Netflix channel.
import json
import os
import subprocess


def validate_task_seven(result=None, device_id=None, backup_dir=None):
    """Verify task 7: netflix in channels.json has initiallyFollowing set to true."""
    file_path = os.path.join(backup_dir, "channels.json") if backup_dir else "channels.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/channels.json"])
    subprocess.run(cmd, stdout=open(file_path, "w"))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
    except:
        return False

    for item in items:
        if isinstance(item, dict) and item.get("id") == "netflix":
            if item.get("initiallyFollowing") == True:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_seven()
    print(result)
