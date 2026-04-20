# Task 33: Mute the first three group chat conversations in order.
import json
import os
import subprocess


def validate_task_thirty_three(result=None, device_id=None, backup_dir=None):
    """Verify task 33: the first three items in group_details.json all have isMuted set to true."""
    file_path = os.path.join(backup_dir, "group_details.json") if backup_dir else "group_details.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/group_details.json"])
    subprocess.run(cmd, stdout=open(file_path, "w"))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
    except:
        return False

    if len(items) < 3:
        return False

    for i in range(3):
        if not isinstance(items[i], dict) or items[i].get("isMuted") != True:
            return False

    return True


if __name__ == "__main__":
    result = validate_task_thirty_three()
    print(result)
