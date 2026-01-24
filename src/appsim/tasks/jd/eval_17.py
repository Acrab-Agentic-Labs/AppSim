import json
import os
import subprocess


def validate_task_seventeen(result=None, device_id=None, backup_dir=None):
    """验证任务十七：帮我在Apple京东自营店购买一件iPhone 15 粉色 256GB"""
    orders_file_path = os.path.join(backup_dir, "orders.json") if backup_dir else "orders.json"

    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.jd_sim", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open(orders_file_path, "w"))

    try:
        with open(orders_file_path, "r", encoding="utf-8") as f:
            orders_data = json.load(f)
    except:
        return False

    # Check the orders for the specific iPhone 15 purchase
    for order in orders_data:
        if order.get("status") == "PENDING_RECEIPT":
            items = order.get("items", [])
            for item in items:
                product = item.get("product", {})
                product_name = product.get("name", "")
                selected_color = item.get("selectedColor", "")
                selected_version = item.get("selectedVersion", "")
                quantity = item.get("quantity", 0)

                # Check for the specific product details
                if (
                    "iPhone 15" in product_name
                    and selected_color == "粉色"
                    and selected_version == "256GB"
                    and quantity == 1
                ):
                    return True

    return False


if __name__ == "__main__":
    result = validate_task_seventeen()
    print(result)
