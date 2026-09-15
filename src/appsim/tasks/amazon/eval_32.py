import json
import os
import subprocess


def verify_requested_item_quantities_added_to_cart(result=None, device_id=None, backup_dir=None):
    """Validate task 32: add 1 'Apple MacBook Air 13-inch with M4 Chip, Space Grey', 2 'Apple MacBook Air 13-inch with M4 Chip, Midnight', and 3 'Apple MacBook Air 13-inch with M4 Chip, Starlight' to the cart."""
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

    if len(items) < 3:
        return False

    expected = [
        {"productName": "Apple MacBook Air 13-inch with M4 Chip, Starlight, M4 / 24GB / 1TB", "quantity": 3},
        {"productName": "Apple MacBook Air 13-inch with M4 Chip, Midnight, M4 / 16GB / 512GB", "quantity": 2},
        {"productName": "Apple MacBook Air 13-inch with M4 Chip, Space Gray, M4 / 16GB / 256GB", "quantity": 2},
    ]

    for i, exp in enumerate(expected):
        item = items[i]
        if not isinstance(item, dict):
            return False
        if item.get("productName") != exp["productName"]:
            return False
        if item.get("quantity") != exp["quantity"]:
            return False

    return True


if __name__ == "__main__":
    result = verify_requested_item_quantities_added_to_cart()
    print(result)
