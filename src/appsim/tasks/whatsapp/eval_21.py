# Task 21: Find the status about Taylor Swift in the Spotify channel and react with a fire emoji.
import json
import os
import subprocess


def validate_task_twenty_one(result=None, device_id=None, backup_dir=None):
    """Verify task 21: status_spotify_003 in statuses.json has userReaction set to 🔥."""
    file_path = os.path.join(backup_dir, "statuses.json") if backup_dir else "statuses.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/statuses.json"])
    subprocess.run(cmd, stdout=open(file_path, "w"))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
    except:
        return False

    for item in items:
        if isinstance(item, dict) and item.get("id") == "status_spotify_003":
            if item.get("userReaction") == "🔥":
                return True

    return False


if __name__ == "__main__":
    result = validate_task_twenty_one()
    print(result)
