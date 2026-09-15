import json
import os
import subprocess


def verify_product_variant_added_to_cart(result=None, device_id=None, backup_dir=None):
    """Validate task 6: select the 12 oz option of Starbucks coffee beans and add it to the cart."""
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
            if item.get("productName") == "Starbucks Pike Place Roast, Whole Bean Coffee, 12 oz":
                return True

    return False


if __name__ == "__main__":
    result = verify_product_variant_added_to_cart()
    print(result)
