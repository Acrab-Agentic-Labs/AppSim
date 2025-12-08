import json
import os
import subprocess


def validate_task_six(result=None, device_id=None, backup_dir=None):
    """验证任务六：结算我的第一个待付款订单后再确认收货。"""
    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders_data = json.load(f)
    except:
        return False

    # 检查订单 order_008 的状态，即第一个待付款订单
    for order in orders_data:
        if order.get("id") == "order_008":
            # 判断该订单的状态是否为 "PENDING_SHIPMENT"（待使用）
            return order.get("status") == "PENDING_SHIPMENT"

    # 如果没有找到 order_008 订单，返回 False
    return False


if __name__ == "__main__":
    result = validate_task_six()
    print(result)
