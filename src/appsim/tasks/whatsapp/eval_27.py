# Task 27: Create a new community named "Book Club" and add the first two contacts.
import json
import os
import subprocess


def validate_task_twenty_seven(result=None, device_id=None, backup_dir=None):
    """Verify task 27: the first item in communities.json has name Book Club and members containing user_010 and user_004."""
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

    if not items:
        return False

    first_item = items[0]
    if not isinstance(first_item, dict):
        return False

    if first_item.get("name") != "Book Club":
        return False

    members = first_item.get("members", [])
    has_user_010 = False
    has_user_004 = False
    for member in members:
        if isinstance(member, dict):
            if member.get("userId") == "user_010":
                has_user_010 = True
            if member.get("userId") == "user_004":
                has_user_004 = True
    if has_user_010 and has_user_004:
        return True

    return False


if __name__ == "__main__":
    result = validate_task_twenty_seven()
    print(result)
