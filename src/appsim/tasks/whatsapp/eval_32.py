# Task 32: Open the channel where Marcus Davis shared his status, send a red heart reaction to that status, then return to the chat and send him "Thanks for sharing!".
import json
import os
import subprocess


def validate_task_thirty_two(result=None, device_id=None, backup_dir=None):
    """Verify task 32: status_rm_001 in statuses.json has userReaction ❤️; the last item in messages.json has conversationId conv_002 and matching textContent."""
    st_path = os.path.join(backup_dir, "statuses.json") if backup_dir else "statuses.json"
    msg_path = os.path.join(backup_dir, "messages.json") if backup_dir else "messages.json"

    cmd1 = ["adb"]
    if device_id:
        cmd1.extend(["-s", device_id])
    cmd1.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/statuses.json"])
    subprocess.run(cmd1, stdout=open(st_path, "w"))

    cmd2 = ["adb"]
    if device_id:
        cmd2.extend(["-s", device_id])
    cmd2.extend(["exec-out", "run-as", "com.example.whatsapp_sim", "cat", "files/data/messages.json"])
    subprocess.run(cmd2, stdout=open(msg_path, "w"))

    try:
        with open(st_path, "r", encoding="utf-8") as f:
            st_data = json.load(f)
            st_items = st_data if isinstance(st_data, list) else []
    except:
        return False

    try:
        with open(msg_path, "r", encoding="utf-8") as f:
            msg_data = json.load(f)
            msg_items = msg_data if isinstance(msg_data, list) else []
    except:
        return False

    status_ok = False
    for item in st_items:
        if isinstance(item, dict) and item.get("id") == "status_rm_001":
            if item.get("userReaction") == "❤️":
                status_ok = True

    if not status_ok:
        return False

    if not msg_items:
        return False

    last_msg = msg_items[-1]
    if isinstance(last_msg, dict) and last_msg.get("conversationId") == "conv_002" and last_msg.get("textContent") == "Thanks for sharing!":
        return True

    return False


if __name__ == "__main__":
    result = validate_task_thirty_two()
    print(result)
