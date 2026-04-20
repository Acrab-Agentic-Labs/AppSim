# Task 23: Add Mia Harris and Noah Kim to the NYC Foodies community.
import json
import os
import subprocess


def validate_task_twenty_three(result=None, device_id=None, backup_dir=None):
    """Verify task 23: NYC Foodies in communities.json has members containing Mia Harris and Noah Kim."""
    file_path = os.path.join(backup_dir, "communities.json") if backup_dir else "communities.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/communities.json"])
    subprocess.run(cmd, stdout=open(file_path, "w"))

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
    except:
        return False

    for item in items:
        if isinstance(item, dict) and item.get("name") == "NYC Foodies":
            members = item.get("members", [])
            has_mia = False
            has_noah = False
            for member in members:
                if isinstance(member, dict):
                    if member.get("displayName") == "Mia Harris":
                        has_mia = True
                    if member.get("displayName") == "Noah Kim":
                        has_noah = True
            if has_mia and has_noah:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_twenty_three()
    print(result)
