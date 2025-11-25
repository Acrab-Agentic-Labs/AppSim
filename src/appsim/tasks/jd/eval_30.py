import json
import os
import subprocess


def validate_task_thirty(result=None, device_id=None, backup_dir=None):
    """验证任务三十：进入Apple产品京东自营旗舰店选择价格最高的商品规格加入购物车并结算，选择赵六的地址。"""
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

    if not orders_data:
        return False

    # Assuming the new order is the last one in the list
    new_order = orders_data[-1]

    # Validation logic
    # Check that items list exists and is not empty
    if not new_order.get("items"):
        return False

    product_details = new_order["items"][0]
    is_version_correct = product_details.get("selectedVersion") == "512GB"
    is_amount_correct = new_order.get("totalAmount") == 10999.0
    is_address_correct = new_order.get("shippingAddress", {}).get("id") == "addr_004"
    is_status_correct = new_order.get("status") == "PENDING_RECEIPT"

    if is_version_correct and is_amount_correct and is_address_correct and is_status_correct:
        return True

    return False


if __name__ == "__main__":
    result = validate_task_thirty()
    print(result)
