import json
import os
import subprocess


TASK25_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页前10个商品中非手机商品的平均评分。",
    "properties": {
        "average_rating": {
            "type": "number",
            "description": "非手机商品的平均评分，保留2位小数，必须是阿拉伯数字。",
        }
    },
    "required": ["average_rating"],
    "additionalProperties": False,
}


def verify_non_phone_product_average_rating(result=None, device_id=None, backup_dir=None):
    """验证任务：统计首页前10个商品中不是手机商品的平均评分,保留2位小数。"""
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

    total_rating = 0
    product_count = 0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)
            first_ten_products = products[:10]
            for product in first_ten_products:
                if product.get("category") != "手机":
                    total_rating += product.get("rating", 0)
                    product_count += 1
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled products.json: {e}")
        return False

    if product_count == 0:
        expected_avg_rating = 0.0
    else:
        expected_avg_rating = round(total_rating / product_count, 2)

    print(f"Expected average rating for non-phone products: {expected_avg_rating}")

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    average_rating = extracted_answer.get("average_rating")
    if average_rating is None:
        return False
    return abs(float(average_rating) - expected_avg_rating) < 0.001
