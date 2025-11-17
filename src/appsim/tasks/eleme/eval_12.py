import json
import subprocess


def validate_change_phone(result=None, device_id=None):
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.myele", "cat", "files/messages.json"])
    subprocess.run(cmd, stdout=open("messages.json", "w"))

    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                data = data[-1] if data else {}
    except:
        return False

    if data.get("action") != "enter_change_phone_page":
        return False
    if data.get("page") != "change_phone":
        return False
    return True


if __name__ == "__main__":
    result = validate_change_phone()
    print(result)
