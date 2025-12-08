import json
import os
import re
import subprocess


def validate_task_twenty_four(result=None, device_id=None, backup_dir=None):
    """验证任务：查看我的订单中，待使用的电子产品共有多少件，给出一个阿拉伯数字即可。"""
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

    expected_count = 0
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
            electronic_categories = ["手机", "电脑", "数码"]
            for order in orders:
                if order.get("status") == "PENDING_SHIPMENT":
                    for item in order.get("items", []):
                        product = item.get("product", {})
                        if product.get("category") in electronic_categories:
                            expected_count += item.get("quantity", 0)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading or parsing pulled orders.json: {e}")
        return False

    print(f"Expected count of PENDING_SHIPMENT electronic items: {expected_count}")

    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        numbers = re.findall(r"\d+", message)
        if str(expected_count) in numbers:
            return True

    return False


if __name__ == "__main__":
    pass
