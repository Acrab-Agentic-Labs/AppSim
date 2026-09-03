# Task 9: buy a white Nintendo Switch now and check out using Amazon Gift Card.

import json
import os
import subprocess


def verify_product_purchased_with_gift_card(result=None, device_id=None, backup_dir=None):
    """Validate task 9: buy a white Nintendo Switch now and check out using Amazon Gift Card."""
    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except:
        return False

    if not isinstance(orders, list) or len(orders) == 0:
        return False

    first_order = orders[0]
    if not isinstance(first_order, dict):
        return False

    # Check the order status and payment method.
    if first_order.get("orderStatus") != "UNSHIPPED":
        return False
    if first_order.get("paymentMethod") != "Gift Card":
        return False

    # Check that the order items include the specified product name.
    items = first_order.get("items", [])
    for item in items:
        if isinstance(item, dict):
            if item.get("productName") == "Nintendo Switch OLED Model - White":
                return True

    return False


if __name__ == "__main__":
    result = verify_product_purchased_with_gift_card()
    print(result)
