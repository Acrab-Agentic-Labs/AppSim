import json
import os
import re
import subprocess


def validate_task_thirteen(result=None, device_id=None, backup_dir=None):
    """验证任务十三：算一下首页全部商品中，评分大于等于4.7的有几个，给出一个阿拉伯数字即可"""
    json_path = os.path.join(backup_dir, "products.json") if backup_dir else "products.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/products.json"])

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
            # 遍历所有商品
            for product in products:
                if product.get("rating", 0) >= 4.7:
                    expected_count += 1
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled products.json: {e}")
        return False

    print(f"Expected count of products with rating >= 4.7: {expected_count}")

    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        # Find all sequences of digits in the message
        numbers = re.findall(r'\\d+', message)
        # Check if the found number is exactly the expected count
        if str(expected_count) in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
