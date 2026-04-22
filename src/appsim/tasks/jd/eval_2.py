import json
import os
import subprocess


def validate_task_two(result=None, device_id=None, backup_dir=None):
    """验证任务二：将首页中的商品iPhone 15 任意颜色 128GB加入购物车。"""
    cart_items_file_path = os.path.join(backup_dir, "cart_items.json") if backup_dir else "cart_items.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/cart_items.json"])
    subprocess.run(cmd, stdout=open(cart_items_file_path, "w"))

    try:
        with open(cart_items_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # cart_items.json是CartItemSpec的数组
            items = data if isinstance(data, list) else []
    except:
        return False

    if not items:
        return False

    last_item = items[-1]
    if not isinstance(last_item, dict):
        return False

    return last_item.get("productName") == "iPhone 15 128GB"


if __name__ == "__main__":
    result = validate_task_two()
    print(result)
