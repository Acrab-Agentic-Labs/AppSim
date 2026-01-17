import json
import os
import subprocess

def eval_26(result=None, device_id=None, backup_dir=None):
    message_file_path = os.path.join(backup_dir, "notes.json") if backup_dir is not None else "notes.json"

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/notes.json"])
        with open(message_file_path, "w") as f:
            subprocess.run(cmd, stdout=f)

        with open(message_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return False

    if result == sum(1 for item in data if item.get("authorId") == "user_002"):
        return  True

if __name__ == "__main__":
    result = eval_26()
    print(result)
