import json
import os
import subprocess


def validate_task_nine(result=None, device_id=None, backup_dir=None):
    """验证任务九：计算购物车中所有商品的总价"""
    json_path = os.path.join(backup_dir, "cart_items.json") if backup_dir else "cart_items.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/cart_items.json"])

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

    if result and "final_message" in result and result["final_message"] is not None:
        message = result["final_message"]
        if str(int(expected_total_price)) in message or str(float(expected_total_price)) in message:
            return True

    return False


if __name__ == "__main__":
    pass
