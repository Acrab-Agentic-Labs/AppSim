import json
import subprocess


def validate_share_malatang(result=None, device_id=None):
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
        all_data = []

    # 检测1: 验证是否进入了全部订单页面
    found_orders_page = False
    for record in all_data:
        if record.get("action") == "enter_orders_page" and record.get("page") == "orders":
            found_orders_page = True
            break

    if not found_orders_page:
        return False

    # 检测2: 验证是否点击了商家名进入商家详情页，且商家名包含"麻辣烫"
    found_navigate_to_malatang_store = False
    for record in all_data:
        if record.get("action") == "navigate_to_store" and record.get("page") == "store_page":
            page_info = record.get("page_info", {})
            restaurant_name = page_info.get("restaurant_name", "")

            # 检查商家名是否包含"麻辣烫"
            if "麻辣烫" in restaurant_name:
                found_navigate_to_malatang_store = True
                break

    if not found_navigate_to_malatang_store:
        return False

    # 检测3: 从数组中找到最后一个分享商家的记录
    share_record = None
    for record in reversed(all_data):
        if record.get("action") == "share_store":
            share_record = record
            break

    # 检测4: 验证分享操作存在
    if share_record is None:
        return False

    # 检测5: 验证page
    if share_record.get("page") != "store_page":
        return False

    # 检测6: 验证extra_data存在且分享平台是微信
    if "extra_data" not in share_record:
        return False

    extra_data = share_record["extra_data"]
    if extra_data.get("platform") != "微信":
        return False

    # 检测7: 验证page_info包含restaurant_name且包含"麻辣烫"
    if "page_info" not in share_record:
        return False

    page_info = share_record["page_info"]
    restaurant_name = page_info.get("restaurant_name", "")

    if "麻辣烫" not in restaurant_name:
        return False

    return True


if __name__ == "__main__":
    # 运行验证并输出结果
    result = validate_share_malatang()
    print(result)
