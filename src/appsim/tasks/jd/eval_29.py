import json
import os
import subprocess


def _load_json_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _get_baseline_orders_path(backup_dir):
    if backup_dir:
        backup_orders_path = os.path.join(backup_dir, "orders.json")
        if os.path.exists(backup_orders_path):
            return backup_orders_path

    return os.path.normpath(
        os.path.join(os.path.dirname(__file__), "..", "app", "src", "main", "assets", "data", "orders.json")
    )


def validate_task_twenty_nine(result=None, device_id=None, backup_dir=None):
    """验证任务：结算总价低于2000的所有待付款订单。"""

    orders_file_path = os.path.join(backup_dir, "orders_after.json") if backup_dir else "orders.json"
    baseline_orders_path = _get_baseline_orders_path(backup_dir)

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        baseline_orders = _load_json_file(baseline_orders_path)
        current_orders = _load_json_file(orders_file_path)
    except Exception as e:
        print(f"Validation Failed: Unable to load orders data. {e}")
        return False

    if not isinstance(baseline_orders, list) or not isinstance(current_orders, list):
        print("Validation Failed: orders.json is not a list.")
        return False

    baseline_orders_map = {order.get("id"): order for order in baseline_orders if isinstance(order, dict)}
    current_orders_map = {order.get("id"): order for order in current_orders if isinstance(order, dict)}

    if len(baseline_orders_map) != len(baseline_orders) or len(current_orders_map) != len(current_orders):
        print("Validation Failed: Duplicate or invalid order entries found.")
        return False

    baseline_order_ids = set(baseline_orders_map.keys())
    current_order_ids = set(current_orders_map.keys())
    if baseline_order_ids != current_order_ids:
        missing_ids = sorted(baseline_order_ids - current_order_ids)
        extra_ids = sorted(current_order_ids - baseline_order_ids)
        print(
            "Validation Failed: Order set changed unexpectedly. "
            f"Missing: {missing_ids}, Extra: {extra_ids}"
        )
        return False

    target_order_ids = {
        order_id
        for order_id, order in baseline_orders_map.items()
        if order.get("status") == "PENDING_PAYMENT" and order.get("totalAmount", 0) < 2000
    }

    changed_order_ids = {
        order_id
        for order_id in baseline_order_ids
        if baseline_orders_map[order_id].get("status") != current_orders_map[order_id].get("status")
    }

    if changed_order_ids != target_order_ids:
        unexpected_changed_ids = sorted(changed_order_ids - target_order_ids)
        unchanged_target_ids = sorted(target_order_ids - changed_order_ids)
        print(
            "Validation Failed: Order status changes do not exactly match the required target set. "
            f"Unexpected changed: {unexpected_changed_ids}, Missing changed targets: {unchanged_target_ids}"
        )
        return False

    for order_id in sorted(target_order_ids):
        current_status = current_orders_map[order_id].get("status")
        if current_status != "PENDING_RECEIPT":
            print(
                f"Validation Failed: Order '{order_id}' status is '{current_status}', "
                "expected 'PENDING_RECEIPT'."
            )
            return False

    for order_id in sorted(baseline_order_ids - target_order_ids):
        baseline_status = baseline_orders_map[order_id].get("status")
        current_status = current_orders_map[order_id].get("status")
        if baseline_status != current_status:
            print(
                f"Validation Failed: Non-target order '{order_id}' status changed from "
                f"'{baseline_status}' to '{current_status}'."
            )
            return False

    return True


if __name__ == "__main__":
    result = validate_task_twenty_nine()
    print(result)
