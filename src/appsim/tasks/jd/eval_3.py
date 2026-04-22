import json
import os
import subprocess


def validate_task_three(result=None, device_id=None, backup_dir=None):
    """验证任务三：立即购买首页中一台任意规格的「iPhone 15」"""
    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"
    log_file_path = os.path.join(backup_dir, "running_status.log") if backup_dir else "running_status.log"

    # Pull orders.json
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except:
        orders = []

    if not isinstance(orders, list) or not orders:
        return False

    first_order = orders[0]
    if not isinstance(first_order, dict):
        return False

    if first_order.get("id") != "order_048":
        return False

    status = first_order.get("status", "")
    items = first_order.get("items", [])
    for item in items:
        if isinstance(item, dict):
            product = item.get("product", {})
            product_name = product.get("name", "") if isinstance(product, dict) else ""
            if "iPhone 15" in product_name and status != "PENDING_PAYMENT":
                return True

    return False


if __name__ == "__main__":
    result = validate_task_three()
    print(result)
