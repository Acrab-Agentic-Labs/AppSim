import json
import os
import subprocess


def validate_task_fifteen(result=None, device_id=None, backup_dir=None):
    """Validate task 15: cancel all pending orders."""
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

    for order in orders:
        if isinstance(order, dict):
            if order.get("orderStatus") == "PENDING":
                return False

    return True


if __name__ == "__main__":
    result = validate_task_fifteen()
    print(result)
