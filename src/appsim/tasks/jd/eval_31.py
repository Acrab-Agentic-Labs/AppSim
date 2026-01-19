import json
import os
import subprocess


def validate_task_thirty_one(result=None, device_id=None, backup_dir=None):
    """验证任务三十一：查看购物车中所有商品，将价格最高的三件商品移出购物车。"""
    cart_items_file_path = os.path.join(backup_dir, "cart_items.json") if backup_dir else "cart_items.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/cart_items.json"])
    subprocess.run(cmd, stdout=open(cart_items_file_path, "w"))

    try:
        with open(cart_items_file_path, "r", encoding="utf-8") as f:
            cart_data = json.load(f)
    except:
        return False

    if not isinstance(cart_data, list):
        return False

    # Check if the specified items are absent
    removed_ids = {"cart_005", "cart_006", "cart_007"}
    for item in cart_data:
        if isinstance(item, dict) and item.get("id") in removed_ids:
            # If any of the targeted items are found, validation fails
            return False

    # If the loop completes without finding any of the targeted items, it means they were all removed.
    return True


if __name__ == "__main__":
    result = validate_task_thirty_one()
    print(f"__result__:{result}")
