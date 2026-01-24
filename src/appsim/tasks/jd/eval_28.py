import json
import os
import subprocess


def validate_task_twenty_eight(result=None, device_id=None, backup_dir=None):
    """验证任务：找到购物车中单价最低的商品购买5件。"""

    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders = json.load(f)
    except:
        return False

    # 查找最新的包含 "五常大米" 的订单
    new_wuchang_rice_order = None
    for order in sorted(orders, key=lambda x: x.get("createTime", 0), reverse=True):
        items = order.get("items", [])
        if any("五常大米" in item.get("product", {}).get("name", "") for item in items):
            new_wuchang_rice_order = order
            break

    if not new_wuchang_rice_order:
        print("Validation Failed: New order for '五常大米' not found.")
        return False

    # 检查订单项的数量和订单状态
    items = new_wuchang_rice_order.get("items", [])
    if not items:
        print("Validation Failed: '五常大米' order has no items.")
        return False

    wuchang_rice_item = next((item for item in items if "五常大米" in item.get("product", {}).get("name", "")), None)

    if (
        wuchang_rice_item
        and wuchang_rice_item.get("quantity") == 5
        and new_wuchang_rice_order.get("status") == "PENDING_RECEIPT"
    ):
        print("Validation Success: New order for '五常大米' found with quantity 5 and status PENDING_RECEIPT.")
        return True
    else:
        print("Validation Failed: '五常大米' order does not meet quantity or status requirements.")
        print(f"Actual quantity: {wuchang_rice_item.get('quantity') if wuchang_rice_item else 'N/A'}")
        print(f"Actual status: {new_wuchang_rice_order.get('status')}")
        return False


if __name__ == "__main__":
    result = validate_task_twenty_eight()
    print(result)
