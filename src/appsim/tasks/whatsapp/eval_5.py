# Task 5: Send a message to the "Friday Night Plans" group chat saying "I feel so excited!!!".
import json
import os
import subprocess


def validate_task_five(result=None, device_id=None, backup_dir=None):
    """Verify task 5: the last item in messages.json has conversationId conv_015 and the expected textContent."""
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
    if isinstance(last_item, dict) and last_item.get("conversationId") == "conv_015" and last_item.get("textContent") == "I feel so excited!!!":
        return True

    return False


if __name__ == "__main__":
    result = validate_task_five()
    print(result)
