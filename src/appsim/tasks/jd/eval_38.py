import json
import os
import subprocess
import time


def validate_task_thirty_eight(result=None, device_id=None, backup_dir=None):
    """验证任务三十八：搜索华为并筛选出起价在4500到5000的手机加入购物车并结算，送到王五的地址。"""

    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    # Pull the orders.json file from the device
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])

    # Give the system some time to write the order to the file
    time.sleep(2)

    try:
        subprocess.run(cmd, stdout=open(orders_file_path, "w"), check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to pull orders.json: {e}")
        return False

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except FileNotFoundError:
        print(f"Validation Failed: orders.json not found at {orders_file_path}")
        return False
    except json.JSONDecodeError:
        print(f"Validation Failed: Could not decode orders.json at {orders_file_path}")
        return False

    # The latest order is the first one in the list (new orders are added at index 0)
    new_order = orders[0] if orders else None

    if not new_order:
        print("Validation Failed: No new order found.")
        return False

    # Verify the order details
    items = new_order.get("items", [])
    if not items:
        print("Validation Failed: New order has no items.")
        return False

    # Assuming only one item is added based on the prompt
    first_item = items[0]
    product_id = first_item.get("product", {}).get("id")
    order_status = new_order.get("status")
    shipping_address_id = new_order.get("shippingAddress", {}).get("id")

    expected_product_id = "huawei_mate60_001"
    expected_status = "PENDING_RECEIPT"
    expected_shipping_address_id = "addr_003" # "王五" is addr_003 based on existing data

    if product_id != expected_product_id:
        print(f"Validation Failed: Product ID mismatch. Expected '{expected_product_id}', Got '{product_id}'.")
        return False

    if order_status != expected_status:
        print(f"Validation Failed: Order status mismatch. Expected '{expected_status}', Got '{order_status}'.")
        return False

    if shipping_address_id != expected_shipping_address_id:
        print(f"Validation Failed: Shipping address ID mismatch. Expected '{expected_shipping_address_id}', Got '{shipping_address_id}'.")
        return False

    print("Validation Success: New order found with correct product, status, and shipping address.")
    return True

if __name__ == "__main__":
    result = validate_task_thirty_eight()
    print(f"__result__:{result}")