import json
import os
import re
import subprocess


def validate_task_twenty_six(result=None, device_id=None, backup_dir=None):
    """验证任务二十六：统计待使用的京东超市的订单总价，保留一位小数。"""
    json_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling orders.json from device: {e}")
        return False

    expected_total_price = 0.0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
            for order in orders:
                if order.get("status") == "PENDING_SHIPMENT":
                    for item in order.get("items", []):
                        product = item.get("product", {})
                        if product.get("storeId") == "jd_supermarket":
                            expected_total_price += order.get("totalAmount", 0)
                            break  # Move to the next order once a match is found
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled orders.json: {e}")
        return False

    expected_total_price = round(expected_total_price, 2)
    print(f"Expected total price for PENDING_SHIPMENT JD Supermarket orders: {expected_total_price}")

    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", message)
        if str(expected_total_price) in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
