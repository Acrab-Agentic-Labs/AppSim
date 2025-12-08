import json
import os
import subprocess


def validate_task_five(result=None, device_id=None, backup_dir=None):
    """验证任务五：首页显示的前十个商品中的手机商品的总价是多少？"""
    json_path = os.path.join(backup_dir, "products.json") if backup_dir else "products.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    # The path is a guess based on the app's asset structure and conventions.
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/products.json"])

    try:
        # Pull the file from the device
        with open(json_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling products.json from device: {e}")
        return False

    # Calculate the expected total price from products.json
    expected_total_price = 0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            products = json.load(f)
            # Take the first 10 products
            first_ten_products = products[:10]
            phone_products = [p for p in first_ten_products if p.get("category") == "手机"]

            # Sum the prices of the phone products among the first 10
            for product in phone_products:
                expected_total_price += product.get("price", 0)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled products.json: {e}")
        return False

    print(f"Expected total price: {expected_total_price}")

    # 检查result中的final_message是否包含相同的数字
    if result and "final_message" in result and result["final_message"] is not None:
        # Check for both integer and float representation
        if str(int(expected_total_price)) in result["final_message"] or str(float(expected_total_price)) in result["final_message"]:
            return True

    return False


if __name__ == "__main__":
    pass