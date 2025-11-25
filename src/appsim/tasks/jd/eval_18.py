import json
import os
import subprocess


def validate_task_eighteen(result=None, device_id=None, backup_dir=None):
    """验证任务十八：取消我的nike待付款订单"""
    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders_data = json.load(f)
    except:
        return False

    # Check for order_012 and its status
    for order in orders_data:
        if order.get("id") == "order_012":
            if order.get("status") == "CANCELLED":
                return True
            else:
                return False  # Found the order, but status is not CANCELLED

    # If order_012 was not found, it means it was deleted or never existed. This also means validation fails.
    return False


if __name__ == "__main__":
    result = validate_task_eighteen()
    print(result)
