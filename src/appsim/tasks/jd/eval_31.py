import json
import os
import subprocess


def _load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_baseline_cart_items_path(backup_dir):
    if backup_dir:
        backup_cart_items_path = os.path.join(backup_dir, "cart_items.json")
        if os.path.exists(backup_cart_items_path):
            return backup_cart_items_path

    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "app", "src", "main", "assets", "data", "cart_items.json")
    )


def _get_cart_item_id(item):
    return item.get("id") if isinstance(item, dict) else None


def _get_cart_item_price(item):
    if not isinstance(item, dict):
        return 0.0

    if "price" in item:
        return float(item.get("price", 0) or 0)

    return float(item.get("product", {}).get("price", 0) or 0)


def validate_task_thirty_one(result=None, device_id=None, backup_dir=None):
    """验证任务三十一：查看购物车中所有商品，将价格最高的三件商品移出购物车。"""
    cart_items_file_path = os.path.join(backup_dir, "cart_items_after.json") if backup_dir else "cart_items.json"
    baseline_cart_items_path = _get_baseline_cart_items_path(backup_dir)

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/cart_items.json"])
    subprocess.run(cmd, stdout=open(cart_items_file_path, "w"))

    try:
        baseline_cart_data = _load_json_file(baseline_cart_items_path)
        current_cart_data = _load_json_file(cart_items_file_path)
    except Exception as e:
        print(f"Validation Failed: Unable to load cart data. {e}")
        return False

    if not isinstance(baseline_cart_data, list) or not isinstance(current_cart_data, list):
        print("Validation Failed: cart_items.json is not a list.")
        return False

    baseline_cart_map = {
        _get_cart_item_id(item): item for item in baseline_cart_data
        if _get_cart_item_id(item) is not None
    }
    current_cart_map = {
        _get_cart_item_id(item): item for item in current_cart_data
        if _get_cart_item_id(item) is not None
    }

    if len(baseline_cart_map) != len(baseline_cart_data) or len(current_cart_map) != len(current_cart_data):
        print("Validation Failed: Duplicate or invalid cart entries found.")
        return False

    sorted_cart_items = sorted(
        baseline_cart_map.values(),
        key=lambda item: (-_get_cart_item_price(item), _get_cart_item_id(item) or "")
    )
    expected_removed_ids = {_get_cart_item_id(item) for item in sorted_cart_items[:3]}

    baseline_cart_ids = set(baseline_cart_map.keys())
    current_cart_ids = set(current_cart_map.keys())
    expected_current_ids = baseline_cart_ids - expected_removed_ids

    if current_cart_ids != expected_current_ids:
        unexpected_removed_ids = sorted((baseline_cart_ids - current_cart_ids) - expected_removed_ids)
        missing_removed_ids = sorted(expected_removed_ids & current_cart_ids)
        unexpected_added_ids = sorted(current_cart_ids - expected_current_ids)
        print(
            "Validation Failed: Cart item set is incorrect after removal. "
            f"Expected removed: {sorted(expected_removed_ids)}, "
            f"Missing removed: {missing_removed_ids}, "
            f"Unexpected removed: {unexpected_removed_ids}, "
            f"Unexpected added: {unexpected_added_ids}"
        )
        return False

    return True


if __name__ == "__main__":
    result = validate_task_thirty_one()
    print(f"__result__:{result}")
