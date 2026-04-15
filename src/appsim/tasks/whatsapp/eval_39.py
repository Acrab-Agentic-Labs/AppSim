# Task 39: Start a call with all contacts whose names start with L, switch it to a video call, keep it going for 10 seconds, then hang up.
import json
import os
import subprocess


def validate_task_thirty_nine(result=None, device_id=None, backup_dir=None):
    """Verify task 39: the first item in calls.json has callType VIDEO, contactIds containing the expected ids, and durationSeconds greater than 10."""
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
    if not isinstance(first_item, dict):
        return False

    if first_item.get("callType") != "VIDEO":
        return False

    contact_ids = first_item.get("contactIds", [])
    if "contact_011" not in contact_ids or "contact_007" not in contact_ids or "contact_017" not in contact_ids:
        return False

    duration = first_item.get("durationSeconds", 0)
    if isinstance(duration, (int, float)) and duration > 10:
        return True

    return False


if __name__ == "__main__":
    result = validate_task_thirty_nine()
    print(result)
