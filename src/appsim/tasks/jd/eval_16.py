import json
import os
import subprocess


def validate_task_sixteen(result=None, device_id=None, backup_dir=None):
    """验证任务十六：将购物车的iPhone15买下来，使用满3000减50的优惠券结算。"""

    cart_items_file_path = os.path.join(backup_dir, "cart_items.json") if backup_dir else "cart_items.json"
    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/cart_items.json"])
    subprocess.run(cmd, stdout=open(cart_items_file_path, "w"))

    try:
        with open(cart_items_file_path, "r", encoding="utf-8") as f:
            cart_items = json.load(f)
    except:
        return False

    iphone_in_cart = any("iPhone 15" in item.get("productName", "") for item in cart_items)
    if iphone_in_cart:
        print("Validation Failed: iPhone 15 is still in the cart.")
        return False

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except:
        return False

    # 查找最新的 iPhone 15 订单
    # 假设它是最新创建的订单，所以我们检查列表的第一个
    new_iphone_order = None
    for order in sorted(orders, key=lambda x: x.get("createTime", 0), reverse=True):
        items = order.get("items", [])
        if any("iPhone 15" in item.get("product", {}).get("name", "") for item in items):
            new_iphone_order = order
            break

    if not new_iphone_order:
        print("Validation Failed: New order for iPhone 15 not found.")
        return False

    # 验证订单金额是否正确应用了优惠券
    # iPhone 15 原价 5999，使用满3000减50优惠券后应为 5949
    expected_total_amount = 5949.0
    actual_total_amount = new_iphone_order.get("totalAmount", 0.0)

    # 允许微小的浮点数误差
    if abs(expected_total_amount - actual_total_amount) > 0.01:
        print(
            f"Validation Failed: Order total is incorrect. Expected: {expected_total_amount}, Actual: {actual_total_amount}"
        )
        return False

    print("Validation Success: iPhone 15 removed from cart and new order created with correct discount.")
    return True


if __name__ == "__main__":
    # For local testing, ensure the device is connected and the app state is correct.
    result = validate_task_sixteen()
    print(f"Validation Result: {result}")
