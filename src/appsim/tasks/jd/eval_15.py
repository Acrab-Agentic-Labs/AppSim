import json
import os
import subprocess


def validate_task_fifteen(result=None, device_id=None, backup_dir=None):
    """验证任务十五：将商品"iPhone 15 蓝色 128GB 1件"、"iPhone 15 黑色 256GB 2件"、"iPhone 15 粉色 128GB 3件"共6件商品加入购物车"""
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
            cart_items = data if isinstance(data, list) else []
    except:
        return False

    # 检查购物车中是否包含这6件商品
    required_items = [
        {"color": "蓝色", "storage": "128GB", "quantity": 1},
        {"color": "黑色", "storage": "256GB", "quantity": 2},
        {"color": "粉色", "storage": "128GB", "quantity": 3},
    ]

    found_items = []
    for required in required_items:
        for item in cart_items:
            if isinstance(item, dict):
                product_name = item.get("productName", "")
                item_color = item.get("color", "")
                item_storage = item.get("storage", "")
                item_quantity = item.get("quantity", 0)

                if (
                    ("iPhone 15" in product_name or "iPhone15" in product_name)
                    and required["color"] == item_color
                    and required["storage"] == item_storage
                    and item_quantity >= required["quantity"]
                ):
                    found_items.append(required)
                    break

    # 如果找到所有3种商品，验证通过
    if len(found_items) == 3:
        return True

    return False


if __name__ == "__main__":
    result = validate_task_fifteen()
    print(result)
