import json
import os
import subprocess


TASK26_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取待使用的京东超市订单总价。",
    "properties": {
        "total_price": {
            "type": "number",
            "description": "京东超市订单总价，保留一位小数，必须是阿拉伯数字。",
        }
    },
    "required": ["total_price"],
    "additionalProperties": False,
}


def verify_store_pending_order_total_price(result=None, device_id=None, backup_dir=None):
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
                            break
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled orders.json: {e}")
        return False

    expected_total_price = round(expected_total_price, 2)
    print(f"Expected total price for PENDING_SHIPMENT JD Supermarket orders: {expected_total_price}")

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_price = extracted_answer.get("total_price")
    if total_price is None:
        return False
    return abs(float(total_price) - expected_total_price) < 0.01
