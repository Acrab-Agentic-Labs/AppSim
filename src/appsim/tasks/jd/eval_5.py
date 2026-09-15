import json
import os
import subprocess


TASK5_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页前十个商品中手机商品的总价。",
    "properties": {
        "total_price": {
            "type": "number",
            "description": "手机商品的总价，必须是阿拉伯数字。",
        }
    },
    "required": ["total_price"],
    "additionalProperties": False,
}


def verify_homepage_phone_products_total_price(result=None, device_id=None, backup_dir=None):
    """验证任务五：首页显示的前十个商品中的手机商品的总价是多少？"""
    json_path = os.path.join(backup_dir, "products.json") if backup_dir else "products.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/products.json"])

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling products.json from device: {e}")
        return False

    expected_total_price = 0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)
            first_ten_products = products[:10]
            phone_products = [p for p in first_ten_products if p.get("category") == "手机"]
            for product in phone_products:
                expected_total_price += product.get("price", 0)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled products.json: {e}")
        return False

    print(f"Expected total price: {expected_total_price}")

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    total_price = extracted_answer.get("total_price")
    if total_price is None:
        return False
    return str(int(expected_total_price)) in str(total_price) or str(float(expected_total_price)) in str(total_price)
