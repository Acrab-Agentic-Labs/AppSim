# Task 35: Enter the first community, check the latest announcement, then go to General and send "Tip: [announcement content]".
import json
import os
import subprocess


def validate_task_thirty_five(result=None, device_id=None, backup_dir=None):
    """Verify task 35: the last item in community_channel_messages.json has the expected conversationId and textContent."""
    file_path = os.path.join(backup_dir, "community_channel_messages.json") if backup_dir else "community_channel_messages.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/community_channel_messages.json"])
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
    if isinstance(last_item, dict) and last_item.get("conversationId") == "community_community_001_general" and last_item.get("textContent") == "Tip\uff1aPlease keep conversation in General and use Announcements for important notices only.":
        return True

    return False


if __name__ == "__main__":
    result = validate_task_thirty_five()
    print(result)
