import json
import subprocess


def validate_task_seventeen(result=None, device_id=None):
    """验证任务十七：进入首页iPhone15商品详情并进入店铺主页，然后立即购买店铺中"iPhone 15 粉色 256GB 1件"后，查看待收货订单"""
    # 读取日志文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/task_seventeen_log.txt"])
    subprocess.run(cmd, stdout=open("task_seventeen_log.txt", "w"))

    # 读取订单文件
    cmd2 = ["adb"]
    if device_id:
        cmd2.extend(["-s", device_id])
    cmd2.extend(["exec-out", "run-as", "com.example.MyJD", "cat", "files/persistent_data/orders.json"])
    subprocess.run(cmd2, stdout=open("orders.json", "w"))

    try:
        with open("task_seventeen_log.txt", "r", encoding="utf-8") as f:
            log_content = f.read()
        with open("orders.json", "r", encoding="utf-8") as f:
            orders_data = json.load(f)
    except:
        return False

    # 检查日志中是否包含关键步骤
    required_steps = ["进入商品详情页", "进入店铺主页", "加载店铺页面数据", "在店铺中选择商品"]
    for step in required_steps:
        if step not in log_content:
            return False

    # 检查订单中是否包含"iPhone 15 粉色 256GB"
    orders = orders_data if isinstance(orders_data, list) else []
    for order in orders:
        if isinstance(order, dict):
            # Order结构: items -> List<OrderItem>, OrderItem结构: product -> Product
            items = order.get("items", [])
            for item in items:
                if isinstance(item, dict):
                    product = item.get("product", {})
                    if isinstance(product, dict):
                        product_name = product.get("name", "")
                        # 检查商品名称和颜色/版本
                        selected_color = item.get("selectedColor", "")
                        selected_version = item.get("selectedVersion", "")
                        if (
                            "iPhone 15" in product_name
                            and "粉色" in (product_name + selected_color)
                            and "256GB" in (product_name + selected_version)
                        ):
                            return True

    return False


if __name__ == "__main__":
    result = validate_task_seventeen()
    print(result)
