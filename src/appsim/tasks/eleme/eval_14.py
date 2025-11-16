import subprocess
import json


def validate_kfc_order(result=None, device_id=None):
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

    # 从数组中找到最后一个完成订单的记录
    order_record = None
    for record in reversed(all_data):
        if record.get("action") == "complete_order":
            order_record = record
            break

    # 检测1: 验证完成订单操作存在
    if order_record is None:
        return False

    # 检测2: 验证page
    if order_record.get("page") != "checkout":
        return False

    # 检测3: 验证extra_data存在
    if "extra_data" not in order_record:
        return False

    extra_data = order_record["extra_data"]

    # 检测4: 【关键】验证搜索了"肯德基"
    if extra_data.get("search_query") != "肯德基":
        return False

    # 检测5: 【关键】验证加入了购物车
    if not extra_data.get("added_to_cart", False):
        return False

    # 检测6: 【关键】验证使用了优惠券
    if not extra_data.get("used_coupon", False):
        return False

    # 检测7: 【关键】验证选择了最大的优惠券
    if not extra_data.get("selected_max_coupon", False):
        return False

    # 检测8: 【关键】验证支付成功
    if not extra_data.get("payment_success", False):
        return False

    return True


if __name__ == "__main__":
    # 运行验证并输出结果
    result = validate_kfc_order()
    print(result)
