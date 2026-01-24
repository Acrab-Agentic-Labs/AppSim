import json
import os
import subprocess


def validate_task_forty(result=None, device_id=None, backup_dir=None):
    """验证任务四十：找到首页前十个商品中评分为4.7的电子商品，选择他们价格最高的规格加入购物车。"""

    cart_items_file_path = os.path.join(backup_dir, "cart_items.json") if backup_dir else "cart_items.json"

    # 使用 adb 拉取购物车文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/cart_items.json"])
    subprocess.run(cmd, stdout=open(cart_items_file_path, "w"))

    try:
        with open(cart_items_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            cart_items = data if isinstance(data, list) else []
    except:
        print("Validation Failed: Unable to read cart_items.json")
        return False

    # 需要检查的商品：评分4.7的电子商品最高规格
    # 1. huawei_p60_001 (评分4.7, 手机类) - Huawei P60 Pro 512GB = 4988.0
    # 2. thinkpad_001 (评分4.7, 电脑类) - 最高规格 = 7499.0
    required_items = [
        {"productId": "huawei_p60_001", "price": 4988.0},
        {"productId": "thinkpad_001", "price": 7499.0},
    ]

    found_items = []
    for required in required_items:
        for item in cart_items:
            if isinstance(item, dict):
                product_id = item.get("productId", "")
                product_price = item.get("price", 0.0)

                # 检查商品ID和价格是否匹配（允许微小的浮点数误差）
                if product_id == required["productId"] and product_price == required["price"]:
                    found_items.append(required)
                    print(f"Found item: {product_id} with price {product_price}")
                    break

    # 如果找到所有2种商品，验证通过
    if len(found_items) == 2:
        print("Validation Success: All required items found in cart.")
        print("  - Huawei P60 001 (4988.0)")
        print("  - ThinkPad 001 (7499.0)")
        return True

    print(f"Validation Failed: Only found {len(found_items)} out of 2 required items.")
    return False


if __name__ == "__main__":
    result = validate_task_forty()
    print(f"Validation Result: {result}")
