# Task 30: Find the status in the Spotify channel about this week's hottest playlist, forward it to the Weekend Hiking Crew group chat, and ask everyone "Which song do you pick?"
import json
import os
import subprocess


def validate_task_thirty(result=None, device_id=None, backup_dir=None):
    """Verify task 30: the last two items in messages.json both have conversationId conv_005, and their textContent values match the expected content respectively."""
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

    if len(items) < 2:
        return False

    second_last = items[-2]
    last = items[-1]

    if not isinstance(second_last, dict) or not isinstance(last, dict):
        return False

    if second_last.get("conversationId") != "conv_005" or last.get("conversationId") != "conv_005":
        return False

    if "This week\u0027s hottest playlist" in (second_last.get("textContent") or "") and last.get("textContent") == "Which song do you pick?":
        return True

    return False


if __name__ == "__main__":
    result = validate_task_thirty()
    print(result)
