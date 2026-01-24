import json
import os
import subprocess


def validate_task_thirty_two(result=None, device_id=None, backup_dir=None):
    """ 验证任务三十二：找到首页前十个商品中价格最低的手机，选择其最便宜的规格购买。 """

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

    # 最新订单在列表的最前面
    latest_order = orders[0]

    items = latest_order.get("items")
    if not items:
        print("Validation Failed: 'items' key not found in the latest order.")
        return False

    order_item = items[0]
    product_info = order_item.get("product", {})

    # 验证 "id"
    expected_id = "huawei_nova11_001"
    actual_id = product_info.get("id")
    if actual_id != expected_id:
        print(f"Validation Failed: Product ID is incorrect. Expected: '{expected_id}', Actual: '{actual_id}'")
        return False

    # 验证 "selectedVersion"
    expected_version = "128GB"
    actual_version = order_item.get("selectedVersion")
    if actual_version != expected_version:
        print(f"Validation Failed: Selected version is incorrect. Expected: '{expected_version}', Actual: '{actual_version}'")
        return False

    print("Validation Success: The cheapest phone (Huawei Nova 11) with the cheapest spec (128GB) was correctly ordered.")
    return True

if __name__ == "__main__":
    result = validate_task_thirty_two()
    print(f"__result__:{result}")
