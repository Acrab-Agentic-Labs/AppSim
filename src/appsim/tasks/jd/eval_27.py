import json
import os
import subprocess


def validate_task_twenty_seven(result=None, device_id=None, backup_dir=None):
    """验证任务：找到我的待收货订单中购买件数最多的商品并确认收货。"""
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

    # 遍历订单数据，查找 order_025
    for order in orders_data:
        if order.get("id") == "order_025":
            # 检查订单状态
            if order.get("status") == "PENDING_SHIPMENT":
                print("Validation successful: Order 'order_025' status is 'PENDING_SHIPMENT'.")
                return True
            else:
                print(
                    f"Validation failed: Order 'order_025' status is '{order.get('status')}', not 'PENDING_SHIPMENT'."
                )
                return False

    print("Validation failed: Order 'order_025' not found in orders.json.")
    return False


if __name__ == "__main__":
    result = validate_task_twenty_seven()
    print(result)
