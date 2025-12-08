import json
import os
import subprocess


def validate_task_thirty_six(result=None, device_id=None, backup_dir=None):
    """ 验证任务三十六：将首页所有华为手机商品的最小的内存版本加入购物车。 """
    cart_items_file_path = os.path.join(backup_dir, "cart_items.json") if backup_dir else "cart_items.json"

    # 从设备拉取购物车文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/cart_items.json"])

    try:
        with open(cart_items_file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"Error pulling cart_items.json from device: {e}")
        return False

    # 读取并验证购物车文件
    try:
        with open(cart_items_file_path, "r", encoding="utf-8") as f:
            cart_items = json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        print("Error reading or parsing cart_items.json")
        return False

    if not isinstance(cart_items, list):
        print("Validation Failed: cart_items.json is not a list.")
        return False

    # 定义需要验证的商品列表
    expected_items = [
        {"productId": "huawei_nova11_001", "storage": "128GB"},
        {"productId": "huawei_mate60_001", "storage": "256GB"},
        {"productId": "huawei_p60_001", "storage": "256GB"},
    ]

    found_count = 0

    # 检查购物车中的每一项是否与预期列表匹配
    for expected in expected_items:
        found = False
        for item in cart_items:
            if (isinstance(item, dict) and
                    item.get("productId") == expected["productId"] and
                    item.get("storage") == expected["storage"]):
                found = True
                break
        if found:
            found_count += 1
        else:
            print(f"Validation Failed: Expected item not found in cart - ProductId: {expected['productId']}, Storage: {expected['storage']}")

    # 验证是否所有预期的商品都已找到
    if found_count == len(expected_items):
        print(f"Validation Success: All {len(expected_items)} expected Huawei phones with minimum storage were found in the cart.")
        return True
    else:
        print(f"Validation Failed: Only found {found_count} out of {len(expected_items)} expected items.")
        return False

if __name__ == "__main__":
    pass
