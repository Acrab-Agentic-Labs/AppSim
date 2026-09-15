import json
import os
import subprocess


def verify_shipped_orders_receipt_confirmed(result=None, device_id=None, backup_dir=None):
    """Validate task 38: confirm receipt for all shipped orders."""
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

    if not isinstance(orders, list):
        return False

    target_order_ids = {"ORD-2024-002", "ORD-2024-006", "ORD-2024-011"}
    found_orders = {}

    for order in orders:
        if isinstance(order, dict):
            order_id = order.get("orderId")
            if order_id in target_order_ids:
                found_orders[order_id] = order.get("orderStatus")

    for order_id in target_order_ids:
        if order_id not in found_orders:
            return False
        if found_orders[order_id] != "DELIVERED":
            return False

    return True


if __name__ == "__main__":
    result = verify_shipped_orders_receipt_confirmed()
    print(result)
