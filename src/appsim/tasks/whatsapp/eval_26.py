# Task 26: Create a new group chat with Rachel Green, Sophia Lee, and Tom Briggs, name it "Project Discussion Group", and send the specified message.
import json
import os
import subprocess


def validate_task_twenty_six(result=None, device_id=None, backup_dir=None):
    """Verify task 26: the last item in group_details.json has groupName Project Discussion Group and the correct memberIds; the last item in messages.json has the expected textContent."""
    gd_path = os.path.join(backup_dir, "group_details.json") if backup_dir else "group_details.json"
    msg_path = os.path.join(backup_dir, "messages.json") if backup_dir else "messages.json"

    cmd1 = ["adb"]
    if device_id:
        cmd1.extend(["-s", device_id])
    cmd1.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/group_details.json"])
    subprocess.run(cmd1, stdout=open(gd_path, "w"))

    cmd2 = ["adb"]
    if device_id:
        cmd2.extend(["-s", device_id])
    cmd2.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/messages.json"])
    subprocess.run(cmd2, stdout=open(msg_path, "w"))

    try:
        with open(gd_path, "r", encoding="utf-8") as f:
            gd_data = json.load(f)
            gd_items = gd_data if isinstance(gd_data, list) else []
    except:
        return False

    try:
        with open(msg_path, "r", encoding="utf-8") as f:
            msg_data = json.load(f)
            msg_items = msg_data if isinstance(msg_data, list) else []
    except:
        return False

    if not gd_items or not msg_items:
        return False

    last_group = gd_items[-1]
    if not isinstance(last_group, dict):
        return False
    if last_group.get("groupName") != "Project Discussion Group":
        return False
    member_ids = last_group.get("memberIds", [])
    if "contact_005" not in member_ids or "contact_010" not in member_ids or "contact_006" not in member_ids:
        return False

    last_msg = msg_items[-1]
    if isinstance(last_msg, dict) and last_msg.get("textContent") == "Hello everyone, welcome to join the project discussion group!":
        return True

    return False


if __name__ == "__main__":
    result = validate_task_twenty_six()
    print(result)
