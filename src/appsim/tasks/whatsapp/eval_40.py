# Task 40: Go to the Netflix channel, find the release date of Black Mirror S7, and tell Sophia Lee the information.
import json
import os
import subprocess


def validate_task_forty(result=None, device_id=None, backup_dir=None):
    """Verify task 40: the last item in messages.json has conversationId conv_008 and textContent containing May 30."""
    file_path = os.path.join(backup_dir, "messages.json") if backup_dir else "messages.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/messages.json"])
    subprocess.run(cmd, stdout=open(file_path, "w"))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
    except:
        return False

    if not items:
        return False

    last_item = items[-1]
    if isinstance(last_item, dict) and last_item.get("conversationId") == "conv_008" and "May 30" in (last_item.get("textContent") or ""):
        return True

    return False


if __name__ == "__main__":
    result = validate_task_forty()
    print(result)
