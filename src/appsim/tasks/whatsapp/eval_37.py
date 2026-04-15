# Task 37: Add a new contact Jessie Brown with the phone number (415) 555-1013, then add her to the SF Tech Squad group chat.
import json
import os
import subprocess


def validate_task_thirty_seven(result=None, device_id=None, backup_dir=None):
    """Verify task 37: contacts.json contains Jessie Brown; SF Tech Squad in group_details.json has memberIds containing contact_018."""
    ct_path = os.path.join(backup_dir, "contacts.json") if backup_dir else "contacts.json"
    gd_path = os.path.join(backup_dir, "group_details.json") if backup_dir else "group_details.json"

    cmd1 = ["adb"]
    if device_id:
        cmd1.extend(["-s", device_id])
    cmd1.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/contacts.json"])
    subprocess.run(cmd1, stdout=open(ct_path, "w"))

    cmd2 = ["adb"]
    if device_id:
        cmd2.extend(["-s", device_id])
    cmd2.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/group_details.json"])
    subprocess.run(cmd2, stdout=open(gd_path, "w"))

    try:
        with open(ct_path, "r", encoding="utf-8") as f:
            ct_data = json.load(f)
            ct_items = ct_data if isinstance(ct_data, list) else []
    except:
        return False

    try:
        with open(gd_path, "r", encoding="utf-8") as f:
            gd_data = json.load(f)
            gd_items = gd_data if isinstance(gd_data, list) else []
    except:
        return False

    contact_ok = False
    for item in ct_items:
        if isinstance(item, dict) and item.get("displayName") == "Jessie Brown" and item.get("phone") == "+1 (415) 555-1013":
            contact_ok = True

    if not contact_ok:
        return False

    for item in gd_items:
        if isinstance(item, dict) and item.get("groupName") == "SF Tech Squad":
            member_ids = item.get("memberIds", [])
            if "contact_018" in member_ids:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_thirty_seven()
    print(result)
