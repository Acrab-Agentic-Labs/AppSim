import json
import os
import subprocess
def verify_collected_note_summarized(result=None, device_id=None, backup_dir=None):

    _USER_ID = "user_current"
    _EXPECTED_COUNT = 1

    message_file_path = (
        os.path.join(backup_dir, "browsing_history.json") if backup_dir is not None else "browsing_history.json"
    )

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/browsing_history.json"])
        with open(message_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if not data or len(data) == 0:
        return False

    # Get user's browsing records, sorted by time
    user_browsing = [item for item in data if item.get("userId") == _USER_ID]

    # Check if recent browsing count meets expectation
    if len(user_browsing) >= _EXPECTED_COUNT:
        # Get the latest records
        recent_browsing = sorted(user_browsing, key=lambda x: x.get("browsedAt", ""), reverse=True)[
                          :_EXPECTED_COUNT
                          ]
        # Verify these records are from home feed
        for item in recent_browsing:
            if item.get("noteId") == "note_008":
                return True
        return False

if __name__ == "__main__":
    result = verify_collected_note_summarized()
    print(result)
