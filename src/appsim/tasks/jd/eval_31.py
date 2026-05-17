import json
import os
import subprocess


def _load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_cart_item_id(item):
    return item.get("id") if isinstance(item, dict) else None


def validate_task_thirty_one(result=None, device_id=None, backup_dir=None):
    """验证任务三十一：查看购物车中所有商品，将价格最高的三件商品移出购物车。"""
    cart_items_file_path = os.path.join(backup_dir, "cart_items_after.json") if backup_dir else "cart_items.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/cart_items.json"])
    subprocess.run(cmd, stdout=open(cart_items_file_path, "w"))

    try:
        current_cart_data = _load_json_file(cart_items_file_path)
    except Exception as e:
        print(f"Validation Failed: Unable to load cart data. {e}")
        return False

    if not isinstance(current_cart_data, list):
        print("Validation Failed: cart_items.json is not a list.")
        return False

    current_cart_map = {
        _get_cart_item_id(item): item for item in current_cart_data
        if _get_cart_item_id(item) is not None
    }

    if len(current_cart_map) != len(current_cart_data):
        print("Validation Failed: Duplicate or invalid cart entries found.")
        return False

    forbidden_ids = {"cart_005", "cart_006", "cart_007"}
    remaining_forbidden_ids = sorted(forbidden_ids & set(current_cart_map.keys()))
    if remaining_forbidden_ids:
        print(
            "Validation Failed: Forbidden cart items still exist after removal. "
            f"Remaining IDs: {remaining_forbidden_ids}"
        )
        return False

    return True


if __name__ == "__main__":
    result = validate_task_thirty_one()
    print(f"__result__:{result}")
