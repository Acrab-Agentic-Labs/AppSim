import json
import os
import subprocess


def validate_task_thirty_nine(result=None, device_id=None, backup_dir=None):
    """验证任务三十九：选择首页电脑中价格最高规格立即购买，送到张三的地址。"""

    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    # 使用 adb 拉取订单文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except:
        print("Validation Failed: Unable to read orders.json")
        return False

    # 查找最新的 ThinkPad 订单
    # 按创建时间倒序排序，查找第一个 ThinkPad 订单
    new_thinkpad_order = None
    for order in sorted(orders, key=lambda x: x.get("createTime", 0), reverse=True):
        items = order.get("items", [])
        if any("thinkpad_001" == item.get("product", {}).get("id", "") for item in items):
            new_thinkpad_order = order
            break

    if not new_thinkpad_order:
        print("Validation Failed: New order for ThinkPad (thinkpad_001) not found.")
        return False

    # 验证订单状态是否为 PENDING_RECEIPT
    order_status = new_thinkpad_order.get("status", "")
    if order_status != "PENDING_RECEIPT":
        print(
            f"Validation Failed: Order status is incorrect. Expected: PENDING_RECEIPT, Actual: {order_status}"
        )
        return False

    # 验证配送地址是否为张三的地址 (addr_001)
    shipping_address = new_thinkpad_order.get("shippingAddress", {})
    address_id = shipping_address.get("id", "")
    if address_id != "addr_001":
        print(
            f"Validation Failed: Shipping address is incorrect. Expected: addr_001, Actual: {address_id}"
        )
        return False

    # 验证订单总金额是否为 7499.0（最高规格价格）
    expected_total_amount = 7499.0
    actual_total_amount = new_thinkpad_order.get("totalAmount", 0.0)

    # 允许微小的浮点数误差
    if abs(expected_total_amount - actual_total_amount) > 0.01:
        print(
            f"Validation Failed: Order total is incorrect. Expected: {expected_total_amount}, Actual: {actual_total_amount}"
        )
        return False

    print("Validation Success: ThinkPad order with highest specification created successfully.")
    print("  - Product ID: thinkpad_001")
    print(f"  - Status: {order_status}")
    print(f"  - Shipping Address: {address_id} (张三)")
    print(f"  - Total Amount: {actual_total_amount}")
    return True


if __name__ == "__main__":
    # For local testing, ensure the device is connected and the app state is correct.
    result = validate_task_thirty_nine()
    print(f"Validation Result: {result}")
