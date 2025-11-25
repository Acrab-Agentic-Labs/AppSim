import json
import os
import subprocess


def find_tie_method(result=None, device_id=None, backup_dir=None):
    """
    Task 2: 我想学习围巾的新系法，帮我推荐一篇笔记并打开
    """
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
        # print(f"❌ Failed to read browsing history file")
        # print(f"   Reason: ADB command failed (return code: {result1.returncode})")
        # if result1.stderr:
        # print(f"   Error: {result1.stderr}")
        return False

    # Parse JSON
    try:
        data = json.loads(result1.stdout)
    except:
        # print(f"❌ Failed to parse browsing history")
        # print(f"   Reason: Invalid JSON format")
        return False

    # Check browsing history
    try:
        # Check if data is empty
        if not data or len(data) == 0:
            # print(f"❌ Browsing history is empty")
            # print(f"   Reason: No browsing records found")
            # print(f"   Expected: At least {expectedCount} browsing records")
            return False

        # Get user's browsing records, sorted by time
        user_browsing = [item for item in data if item.get("_USER_ID") == _USER_ID]

        if len(user_browsing) == 0:
            return False

        # Get the latest record
        latest_record = sorted(user_browsing, key=lambda x: x.get("browsedAt", ""), reverse=True)[0]

        # Check if noteTitle contains "围巾系法"
        if "围巾系法" in latest_record.get("noteTitle", ""):
            return True
        else:
            return False

    except Exception:
        # print(f"❌ Error while checking browsing history")
        # print(f"   Reason: {e}")
        return False


if __name__ == "__main__":
    print(find_tie_method())
