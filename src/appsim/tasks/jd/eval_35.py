import json
import os
import subprocess


def validate_task_thirty_five(result=None, device_id=None, backup_dir=None):
    """ 验证任务三十五：进入华为官方旗舰店选择评分最高的商品加入购物车并结算，选择李四的地址。 """
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

    # 假设最新订单在列表的最前面
    latest_order = orders[0]

    # 验证 shippingAddress id
    shipping_address = latest_order.get("shippingAddress", {})
    actual_address_id = shipping_address.get("id")
    expected_address_id = "addr_002"

    if actual_address_id != expected_address_id:
        print(f"Validation Failed: Shipping address ID is incorrect. Expected: '{expected_address_id}', Actual: '{actual_address_id}'")
        return False

    # 验证 items 中的 product id
    items = latest_order.get("items")
    if not items:
        print("Validation Failed: 'items' key not found in the latest order.")
        return False

    product_info = items[0].get("product", {})
    actual_product_id = product_info.get("id")
    expected_product_id = "huawei_mate60_001"

    if actual_product_id != expected_product_id:
        print(f"Validation Failed: Product ID is incorrect. Expected: '{expected_product_id}', Actual: '{actual_product_id}'")
        return False

    print("Validation Success: Correct product (huawei_mate60_001) and shipping address (addr_002) found in the latest order.")
    return True

if __name__ == "__main__":
    result = validate_task_thirty_five()
    print(f"__result__:{result}")