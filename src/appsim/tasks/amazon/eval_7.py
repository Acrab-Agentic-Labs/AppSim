import json
import os
import subprocess


def verify_shopping_list_created(result=None, device_id=None, backup_dir=None):
    """Validate task 7: create a new shopping list named 'My Amazon List'."""
    lists_data_file_path = os.path.join(backup_dir, "lists_data.json") if backup_dir else "lists_data.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/lists_data.json"])
    subprocess.run(cmd, stdout=open(lists_data_file_path, "w"))

    try:
        with open(lists_data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            lists = data if isinstance(data, list) else []
    except:
        return False

    for item in lists:
        if isinstance(item, dict):
            if item.get("listName") == "My Amazon List":
                return True

    return False


if __name__ == "__main__":
    result = verify_shopping_list_created()
    print(result)
