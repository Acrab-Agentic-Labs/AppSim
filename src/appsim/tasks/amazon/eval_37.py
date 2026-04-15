import json
import os
import subprocess


def validate_task_thirty_seven(result=None, device_id=None, backup_dir=None):
    """Validate task 37: create a shopping list named 'Electronics Wishlist', then search for 'Samsung' and add the first search result to that list."""
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

    for lst in lists:
        if isinstance(lst, dict) and lst.get("listName") == "Electronics Wishlist":
            product_ids = lst.get("productIds", [])
            if "prod_006" in product_ids:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_thirty_seven()
    print(result)
