import json
import os
import re
import subprocess


def validate_task_twenty_three(result=None, device_id=None, backup_dir=None):
    """验证任务二十三：计算Apple官方旗舰店评分大于4.7的商品的平均价格，保留一位小数。"""
    json_path = os.path.join(backup_dir, "shop_data.json") if backup_dir else "shop_data.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/shop_data.json"])

    try:
        with open(json_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling shop_data.json from device: {e}")
        return False

    total_price = 0
    product_count = 0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            shop_data = json.load(f)
            products = shop_data.get("products", [])
            for product in products:
                if (
                        product.get("storeId") == "apple_jd_flagship"
                        and product.get("rating", 0) > 4.7
                ):
                    total_price += product.get("price", 0)
                    product_count += 1
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled shop_data.json: {e}")

    if product_count == 0:
        expected_avg_price = 0.0
    else:
        expected_avg_price = round(total_price / product_count, 1)

    print(f"Expected average price: {expected_avg_price}")

    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        # Find all numbers (including floats)
        numbers = re.findall(r"[-+]?\d*\.\d+|\d+", message)
        if str(expected_avg_price) in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
 