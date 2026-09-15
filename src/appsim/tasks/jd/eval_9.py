import json
import os
import subprocess


TASK9_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取购物车中所有商品的总价。",
    "properties": {
        "total_price": {
            "type": "number",
            "description": "购物车中所有商品的总价，必须是阿拉伯数字。",
        }
    },
    "required": ["total_price"],
    "additionalProperties": False,
}


def verify_cart_total_price(result=None, device_id=None, backup_dir=None):
    """验证任务九：计算购物车中所有商品的总价"""
    json_path = os.path.join(backup_dir, "cart_items.json") if backup_dir else "cart_items.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/cart_items.json"])

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling cart_items.json from device: {e}")
        return False

    expected_total_price = 0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            cart_items = json.load(f)
            for item in cart_items:
                price = item.get("price", 0)
                quantity = item.get("quantity", 0)
                expected_total_price += price * quantity
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled cart_items.json: {e}")
        return False

    print(f"Expected total cart price: {expected_total_price}")

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_price = extracted_answer.get("total_price")
    if total_price is None:
        return False
    return str(int(expected_total_price)) in str(total_price) or str(float(expected_total_price)) in str(total_price)
