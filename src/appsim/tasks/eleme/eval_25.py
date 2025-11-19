import json
import subprocess


# 验证任务25: 进入"我的"-"我的订单",找到最新已完成订单,点击进入第一个订单详情页,查看"实付"金额明细
# 关键验证点:
# 1. 必须进入全部订单页(my_orders页面)
# 2. 必须点击页面第一个订单(进入订单详情页)
def validate_view_first_order_detail(result=None, device_id=None):
    # 从设备获取文件
    cmd = ["adb"]
    if device_id:
        cmd.extend(["-s", device_id])
    cmd.extend(["exec-out", "run-as", "com.example.myele", "cat", "files/messages.json"])
    subprocess.run(cmd, stdout=open("messages.json", "w"))

    # 读取文件
    try:
        with open("messages.json", "r", encoding="utf-8") as f:
            all_data = json.load(f)
    except:
        return False

    # 检查是否有数据
    if not all_data:
        return False

    # 检测1: 验证进入全部订单页面(my_orders)
    enter_orders_page = False
    for record in all_data:
        # 支持两种格式：enter_orders_page/orders 或 navigate/my_orders
        if (record.get("action") == "enter_orders_page" and record.get("page") == "orders") or (
            record.get("action") == "navigate" and record.get("page") == "my_orders"
        ):
            extra_data = record.get("extra_data", {})
            # 检查是否显示全部订单(默认或明确指定tab为"全部"或"all")
            # 支持两个字段名：selected_tab 或 tab
            tab = extra_data.get("selected_tab") or extra_data.get("tab", "全部")
            if tab in ["全部", "all", "ALL"]:
                enter_orders_page = True
                break

    if not enter_orders_page:
        return False

    # 检测2: 验证点击第一个已送达订单进入订单详情页
    clicked_first_delivered_order = False
    for record in all_data:
        if record.get("action") == "navigate" and record.get("page") == "order_detail":
            extra_data = record.get("extra_data", {})
            # 验证是否从my_orders页面来的
            from_page = extra_data.get("from_page", "")
            # 验证是否是第一个订单(order_index = 0 或 is_first_order = True)
            order_index = extra_data.get("order_index", -1)
            is_first_order = extra_data.get("is_first_order", False)
            # 验证订单状态是否是已送达
            order_status = extra_data.get("order_status", "")

            if from_page == "my_orders" and (order_index == 0 or is_first_order) and order_status == "已送达":
                clicked_first_delivered_order = True
                break

    if not clicked_first_delivered_order:
        return False

    # 检测3: 验证result中是否包含"33"
    if result is None:
        return False
    if "final_message" in result and "33" in result["final_message"]:
        return True
    else:
        return False


if __name__ == "__main__":
    # 运行验证并输出结果
    result = validate_view_first_order_detail()
    print(result)
