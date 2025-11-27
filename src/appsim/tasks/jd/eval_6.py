import json
import os
import subprocess


def validate_task_six(result=None, device_id=None, backup_dir=None):
    """验证任务六：结算我的第一个待付款订单"""
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

    # 检查第一个订单的状态
    if orders_data:
        first_order = orders_data[0]
        if first_order.get("id") == "order_008" and first_order.get("status") in ["PENDING_SHIPMENT", "PENDING_RECEIPT"]:
            return True

    return False


if __name__ == "__main__":
    result = validate_task_six()
    print(result)
