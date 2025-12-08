import json
import os
import subprocess


def validate_task_thirty_seven(result=None, device_id=None, backup_dir=None):
    """ 验证任务三十七：购买首页华为商品中买家评价最多的商品。 """
    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    # 从设备拉取订单文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])

    try:
        with open(orders_file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling orders.json from device: {e}")
        return False

    # 读取并验证订单文件
    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error reading or parsing orders.json")
        return False

    if not orders:
        print("Validation Failed: orders.json is empty.")
        return False

    # 假设最新订单在列表的最前面 (sorted by creationTime descending by default in the app)
    latest_order = orders[0]

    # 1. 验证订单状态
    expected_status = "PENDING_RECEIPT"
    actual_status = latest_order.get("status")

    if actual_status != expected_status:
        print(f"Validation Failed: Order status is incorrect. Expected: '{expected_status}', Actual: '{actual_status}'")
        return False

    # 2. 验证 items 中的 product id
    items = latest_order.get("items")
    if not items:
        print("Validation Failed: 'items' key not found in the latest order.")
        return False

    product_info = items[0].get("product", {})
    actual_product_id = product_info.get("id")
    expected_product_id = "huawei_p60_001"

    if actual_product_id != expected_product_id:
        print(f"Validation Failed: Product ID is incorrect. Expected: '{expected_product_id}', Actual: '{actual_product_id}'")
        return False

    print("Validation Success: The correct product (huawei_p60_001) was ordered and the status is PENDING_RECEIPT.")
    return True

if __name__ == "__main__":
    pass