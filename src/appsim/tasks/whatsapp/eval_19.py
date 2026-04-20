# Task 19: Mute notifications for the first conversation in the chat list, then return to the list and confirm that the mute icon is shown.
import json
import os
import subprocess


def validate_task_nineteen(result=None, device_id=None, backup_dir=None):
    """Verify task 19: the first item in group_details.json has isMuted set to true."""
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

    if not items:
        return False

    first_item = items[0]
    if isinstance(first_item, dict) and first_item.get("isMuted") == True:
        return True

    return False


if __name__ == "__main__":
    result = validate_task_nineteen()
    print(result)
