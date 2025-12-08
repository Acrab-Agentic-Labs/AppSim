import json
import os
import subprocess


def validate_task_twenty_nine(result=None, device_id=None, backup_dir=None):
    """验证任务：结算总价低于2000的所有待付款订单。"""

    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except:
        return False

    target_order_ids = ["order_009", "order_010", "order_012", "order_014", "order_015"]
    all_checked_pass = True

    orders_map = {order.get("id"): order for order in orders}

    for order_id in target_order_ids:
        order = orders_map.get(order_id)
        if order is None:
            print(f"Validation Failed: Order '{order_id}' not found in orders.json.")
            all_checked_pass = False
            break

        current_status = order.get("status")
        if current_status != "PENDING_RECEIPT":
            print(f"Validation Failed: Order '{order_id}' status is '{current_status}', expected 'PENDING_RECEIPT'.")
            all_checked_pass = False
            break
        else:
            print(f"Order '{order_id}' status is correct: 'PENDING_RECEIPT'.")

    return all_checked_pass


if __name__ == "__main__":
    result = validate_task_twenty_nine()
    print(result)
