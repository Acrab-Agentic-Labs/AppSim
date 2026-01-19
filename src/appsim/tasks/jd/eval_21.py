import json
import os
import re
import subprocess


def validate_task_twenty_one(result=None, device_id=None, backup_dir=None):
    """验证任务：在Apple官方旗舰店筛选出价格在6000.0至8000.0的手机类别商品有多少个，给出一个阿拉伯数字即可。"""
    json_path = os.path.join(backup_dir, "apple_shop_data.json") if backup_dir else "apple_shop_data.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/apple_shop_data.json"])

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling apple_shop_data.json from device: {e}")
        return False

    expected_count = 0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            products = data.get("products", [])
            for product in products:
                if (
                        product.get("category") == "手机"
                        and 6000.0 <= product.get("price", 0) <= 8000.0
                ):
                    expected_count += 1
                    print(f"Found: {product.get('name')} - {product.get('price')}")
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled apple_shop_data.json: {e}")
        return False

    print(f"Expected count of filtered products: {expected_count}")

    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        numbers = re.findall(r"\d+", message)
        if str(expected_count) in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
