import json
import subprocess


def validate_task_three(result=None, device_id=None):
    """验证任务三：立即购买首页中一台任意规格的「iPhone 15」"""
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd, stdout=open("orders.json", "w"))

    try:
        with open("orders.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            # orders.json是Order的数组
            orders = data if isinstance(data, list) else []
    except:
        return False

    # 检查订单中是否包含iPhone 15商品购买订单
    for order in orders:
        if isinstance(order, dict):
            # Order结构: items -> List<OrderItem>, OrderItem结构: product -> Product
            items = order.get("items", [])
            for item in items:
                if isinstance(item, dict):
                    product = item.get("product", {})
                    product_name = product.get("name", "") if isinstance(product, dict) else ""
                    if "iPhone 15" in product_name:
                        return True

    return False


if __name__ == "__main__":
    result = validate_task_three()
    print(result)
