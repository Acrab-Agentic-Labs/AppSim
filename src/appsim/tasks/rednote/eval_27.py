# eval_27.py
import json
import os
import subprocess


def find_tie_method(result=None, device_id=None, backup_dir=None):
    _USER_ID = "user_current"
    message_file_path = os.path.join(backup_dir, "browsing_history.json") if backup_dir else "browsing_history.json"

    # Get browsing history from device
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(
        ["exec-out", "run-as", "com.example.test05", "cat", "files/browsing_history.json"],
    )
    result1 = subprocess.run(cmd, capture_output=True, encoding="utf-8", errors="replace")

    # Check if command executed successfully
    if result1.returncode != 0 or not result1.stdout:
        return False

    # Parse JSON
    try:
        data = json.loads(result1.stdout)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    # Check if data is empty
    if not data or len(data) == 0:
        return False

    # Get user's browsing records, sorted by time
    user_browsing = [item for item in data if item.get("userId") == _USER_ID]

    if len(user_browsing) == 0:
        return False

    # Get the latest record
    latest_record = sorted(user_browsing, key=lambda x: x.get("browsedAt", ""), reverse=True)[0]

    # Check if noteTitle contains "围巾系法"
    if "围巾系法" in latest_record.get("noteTitle", ""):
        return True
    else:
        return False


if __name__ == "__main__":
    print(find_tie_method())