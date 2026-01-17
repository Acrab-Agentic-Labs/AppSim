import json
import os
import subprocess

def eval_24(result=None, device_id=None, backup_dir=None):
    def eval_24(result=None, device_id=None, backup_dir=None):
        message_file_path = os.path.join(backup_dir, "messages.json") if backup_dir is not None else "messages.json"

        try:
            cmd = ["adb"]
            if device_id:
                cmd.extend(["-s", device_id])
            cmd.extend(["exec-out", "run-as", "com.example.rednote_sim", "cat", "files/messages.json"])
            with open(message_file_path, "w") as f:
                subprocess.run(cmd, stdout=f)

            with open(message_file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return False

        if not data or len(data) == 0:
            return False

        if result == len(data):
            return True

    if __name__ == "__main__":
        result = eval_24()
        print(result)


if __name__ == "__main__":
    result = eval_24()
    print(result)
