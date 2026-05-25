import json
import os
import subprocess


TASK8_ANSWER_SCHEMA = {
    "type": "object",
    "description": "提取首页前十个商品中手机的数量。",
    "properties": {
        "phone_count": {
            "type": "integer",
            "description": "手机商品的数量，必须是阿拉伯数字整数。",
        }
    },
    "required": ["phone_count"],
    "additionalProperties": False,
}


def validate_task_eight(result=None, device_id=None, backup_dir=None):
    """验证任务八：计算首页展示的商品中前十个有多少个是手机，给出一个阿拉伯数字即可。"""
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
            first_ten_products = products[:10]
            phone_products = [p for p in first_ten_products if p.get("category") == "手机"]
            expected_count = len(phone_products)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled products.json: {e}")
        return False

    print(f"Expected phone count: {expected_count}")

    if not isinstance(result, dict):
        return False
    extracted_answer = result.get("extracted_answer")
    if not isinstance(extracted_answer, dict):
        return False
    phone_count = extracted_answer.get("phone_count")
    if phone_count is None:
        return False
    return int(phone_count) == expected_count
