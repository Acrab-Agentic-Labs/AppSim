# Task 18: Start a call with Ethan Garcia and Lucas Anderson, then hang up.
import json
import os
import subprocess


def validate_task_eighteen(result=None, device_id=None, backup_dir=None):
    """Verify task 18: the first item in calls.json has contactIds containing contact_013 and contact_017."""
    file_path = os.path.join(backup_dir, "calls.json") if backup_dir else "calls.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/calls.json"])
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
    if isinstance(first_item, dict):
        contact_ids = first_item.get("contactIds", [])
        if "contact_013" in contact_ids and "contact_017" in contact_ids:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_eighteen()
    print(result)
