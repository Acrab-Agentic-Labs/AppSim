import json
import os
import subprocess


def validate_task_two(result=None, device_id=None, backup_dir=None):
    """验证任务二：将首页中的商品「iPhone 15 蓝色 128GB」加入购物车"""
    cart_items_file_path = os.path.join(backup_dir, "cart_items.json") if backup_dir else "cart_items.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/cart_items.json"])
    subprocess.run(cmd, stdout=open(cart_items_file_path, "w"))

    try:
        with open(cart_items_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # cart_items.json是CartItemSpec的数组
            items = data if isinstance(data, list) else []
    except:
        return False

    # 检查购物车中是否包含"Apple/苹果 iPhone 15 (A3092) 128GB"
    for item in items:
        if isinstance(item, dict):
            product_name = item.get("productName", "")
            # 检查是否匹配完整商品名称
            if "Apple/苹果 iPhone 15 (A3092) 128GB" in product_name:
                return True

    return False


if __name__ == "__main__":
    result = validate_task_two()
    print(result)
