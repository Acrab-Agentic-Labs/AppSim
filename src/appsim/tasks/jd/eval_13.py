import json
import os
import subprocess


TASK13_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页商品中评分大于等于4.7的商品数量。",
    "properties": {
        "product_count": {
            "type": "integer",
            "description": "评分大于等于4.7的商品数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["product_count"],
    "additionalProperties": False,
}


def validate_task_thirteen(result=None, device_id=None, backup_dir=None):
    """验证任务十三：算一下首页全部商品中，评分大于等于4.7的有几个，给出一个阿拉伯数字即可"""
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

    expected_count = 0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)
            for product in products:
                if product.get("rating", 0) >= 4.7:
                    expected_count += 1
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled products.json: {e}")
        return False

    print(f"Expected count of products with rating >= 4.7: {expected_count}")

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    product_count = extracted_answer.get("product_count")
    if product_count is None:
        return False
    return int(product_count) == expected_count
