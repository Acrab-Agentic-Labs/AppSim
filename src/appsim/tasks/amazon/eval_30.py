import json
import os
import subprocess


def verify_shopping_list_created_with_home_items(result=None, device_id=None, backup_dir=None):
    """Validate task 30: create a new shopping list named 'Coffee' and add the coffee-related items from the home page to that list."""
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
        if isinstance(lst, dict) and lst.get("listName") == "Coffee":
            product_ids = lst.get("productIds", [])
            if "prod_008" in product_ids and "prod_014" in product_ids:
                return True

    return False


if __name__ == "__main__":
    result = verify_shopping_list_created_with_home_items()
    print(result)
