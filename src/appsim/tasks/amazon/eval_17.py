import json
import os
import subprocess


def verify_low_price_cart_items_removed(result=None, device_id=None, backup_dir=None):
    """Validate task 17: remove all items priced below $200 from the cart."""
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

    for item in items:
        if isinstance(item, dict):
            price = item.get("price", 0)
            if isinstance(price, (int, float)) and price < 200:
                return False

    return True


if __name__ == "__main__":
    result = verify_low_price_cart_items_removed()
    print(result)
