import json
import os
import subprocess


def validate_task_eleven(result=None, device_id=None, backup_dir=None):
    """Validate task 11: find the highest-rated product in the 'Lifestyle' category and add it to the cart."""
    cart_data_file_path = os.path.join(backup_dir, "cart_data.json") if backup_dir else "cart_data.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/cart_data.json"])
    subprocess.run(cmd, stdout=open(cart_data_file_path, "w"))

    try:
        with open(cart_data_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            items = data if isinstance(data, list) else []
    except:
        return False

    if not items:
        return False

    first_item = items[0]
    if isinstance(first_item, dict) and first_item.get("productId") == "prod_009":
        return True

    return False


if __name__ == "__main__":
    result = validate_task_eleven()
    print(result)
