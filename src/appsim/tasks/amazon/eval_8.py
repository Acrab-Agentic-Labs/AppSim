import json
import os
import subprocess


def validate_task_eight(result=None, device_id=None, backup_dir=None):
    """Validate task 8: delete the fourth shipping address (addr_004)."""
    addresses_file_path = os.path.join(backup_dir, "addresses.json") if backup_dir else "addresses.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/addresses.json"])
    subprocess.run(cmd, stdout=open(addresses_file_path, "w"))

    try:
        with open(addresses_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            addresses = data if isinstance(data, list) else []
    except:
        return False

    for address in addresses:
        if isinstance(address, dict):
            if address.get("id") == "addr_004":
                return False

    return True


if __name__ == "__main__":
    result = validate_task_eight()
    print(result)
