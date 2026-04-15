import json
import os
import subprocess


def validate_task_twelve(result=None, device_id=None, backup_dir=None):
    """Validate task 12: buy a watch from the home page right away, choose the lowest-priced option, and have it shipped to Sarah Davis's address."""
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

    if first_order.get("orderStatus") != "UNSHIPPED":
        return False

    shipping_address = first_order.get("shippingAddress", {})
    if not isinstance(shipping_address, dict):
        return False
    if shipping_address.get("id") != "addr_004":
        return False

    items = first_order.get("items", [])
    for item in items:
        if isinstance(item, dict):
            if item.get("productId") == "prod_006" and item.get("price") == 279.99:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_twelve()
    print(result)
