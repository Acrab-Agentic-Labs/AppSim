# Task 16: Forward the most commented status from the Netflix channel to Emily Chen.
import json
import os
import subprocess


def validate_task_sixteen(result=None, device_id=None, backup_dir=None):
    """Verify task 16: the last item in messages.json has conversationId conv_003 and the expected textContent."""
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
    expected_text = "🎬 First look: Stranger Things Season 5 official trailer is here! The Upside Down awaits... 👀 #StrangerThings5"
    if isinstance(last_item, dict) and last_item.get("conversationId") == "conv_003" and last_item.get("textContent") == expected_text:
        return True

    return False


if __name__ == "__main__":
    result = validate_task_sixteen()
    print(result)
