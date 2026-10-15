import json
import os
import subprocess


# Orders seeded as PENDING by the app (assets/data/orders.json in AppSim-Amazon).
BASELINE_PENDING_ORDER_IDS = {"ORD-2024-005", "ORD-2024-012"}


def _load_baseline_pending_order_ids():
    return set(BASELINE_PENDING_ORDER_IDS)


def verify_pending_orders_canceled(result=None, device_id=None, backup_dir=None):
    """Validate task 15: cancel all pending orders."""
    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.amazon_sim", "cat", "files/orders.json"])
    with open(orders_file_path, "w", encoding="utf-8") as output_file:
        subprocess.run(cmd, stdout=output_file)

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except Exception:
        return False

    if not isinstance(orders, list):
        return False

    baseline_pending_order_ids = _load_baseline_pending_order_ids()
    if not baseline_pending_order_ids:
        return False

    current_status_by_order_id = {}
    for order in orders:
        if not isinstance(order, dict):
            continue

        order_id = order.get("orderId")
        order_status = order.get("orderStatus")

        if order_status == "PENDING":
            return False

        if order_id:
            current_status_by_order_id[order_id] = order_status

    for order_id in baseline_pending_order_ids:
        if current_status_by_order_id.get(order_id) != "CANCELED":
            return False

    return True


if __name__ == "__main__":
    result = verify_pending_orders_canceled()
    print(result)
