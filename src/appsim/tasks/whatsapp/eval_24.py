# Task 24: Start a video call in the Weekend Hiking Crew group chat, keep it going for more than 5 seconds, then hang up.
import json
import os
import subprocess


def validate_task_twenty_four(result=None, device_id=None, backup_dir=None):
    """Verify task 24: the first item in calls.json has conversationId conv_005 and durationSeconds greater than 5."""
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
    if isinstance(first_item, dict) and first_item.get("conversationId") == "conv_005":
        duration = first_item.get("durationSeconds", 0)
        if isinstance(duration, (int, float)) and duration > 5:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_twenty_four()
    print(result)
