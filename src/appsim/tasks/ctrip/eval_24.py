import json
import re
import subprocess
from datetime import date
import os

# 任务24：进入 "机票" 页面，查10月21日从北京飞广州的机票，统计下最便宜的 3 趟航班的平均价格
# 检查条件：智能体计算的平均价格是否与真实的平均价格一致


def calculate_day_price(target_date, base_price):
    """
    计算特定日期的基础价格
    根据FlightListTabModel.kt中的calculateDayPrice函数逻辑
    """
    day_of_month = target_date.day
    final_price = base_price

    # 日期在10月20-25号范围内的价格调整
    if day_of_month == 20:
        final_price += 0  # 周日，正常价格
    elif day_of_month == 21:
        final_price -= 10  # 周一，工作日优惠
    elif day_of_month == 22:
        final_price -= 15  # 周二，工作日最优惠
    elif day_of_month == 23:
        final_price -= 5  # 周三，工作日优惠
    elif day_of_month == 24:
        final_price += 10  # 周四，接近周末
    elif day_of_month == 25:
        final_price += 20  # 周五，周末前涨价

    return final_price


def get_beijing_to_guangzhou_flights(target_date):
    """
    获取北京到广州的所有航班数据
    根据FlightListTabModel.kt中的generateBeijingToGuangzhouFlights函数
    """
    day_price = calculate_day_price(target_date, 380)
    business_price = day_price * 3

    flights = [
        # 经济舱航班
        {
            "id": f"BJS_CAN_{target_date}_1",
            "flightNumber": "CZ3101",
            "departureTime": "10:30",
            "arrivalTime": "14:15",
            "airline": "南航",
            "price": day_price,
            "cabinClass": "economy",
        },
        {
            "id": f"BJS_CAN_{target_date}_2",
            "flightNumber": "CA1301",
            "departureTime": "15:45",
            "arrivalTime": "19:30",
            "airline": "国航",
            "price": day_price + 25,
            "cabinClass": "economy",
        },
        # 公务/头等舱航班
        {
            "id": f"BJS_CAN_{target_date}_3",
            "flightNumber": "CZ3115",
            "departureTime": "08:15",
            "arrivalTime": "12:00",
            "airline": "南航",
            "price": business_price,
            "cabinClass": "business",
        },
        {
            "id": f"BJS_CAN_{target_date}_4",
            "flightNumber": "CA1315",
            "departureTime": "18:20",
            "arrivalTime": "22:05",
            "airline": "国航",
            "price": business_price + 200,
            "cabinClass": "business",
        },
    ]

    return flights


def get_expected_average_price_top3():
    """
    计算真实答案：10月21日北京到广州最便宜的3趟航班的平均价格
    """
    # 10月21日
    target_date = date(2025, 10, 21)

    # 获取所有航班
    flights = get_beijing_to_guangzhou_flights(target_date)

    # 按价格排序
    sorted_flights = sorted(flights, key=lambda x: x["price"])

    # 取最便宜的3趟
    top3 = sorted_flights[:3]

    # 计算平均价格
    total_price = sum(flight["price"] for flight in top3)
    average_price = total_price / 3

    return average_price, top3


def check_flight_search_price_avg(result=None, device_id=None):
    """
    检验函数：验证智能体答案是否正确

    参数:
        agent_answer: 智能体生成的答案，可以是：
                     - 数字: 625 或 625.0
                     - 字符串: "625" 或 "¥625"
                     - 包含平均价格的字典: {"average_price": 625}

    返回:
        True: 验证成功（允许±1元的误差）
        False: 验证失败
    """
    agent_answer = result
    # 计算真实答案
    expected_avg, _ = get_expected_average_price_top3()

    # 处理不同类型的智能体答案
    try:
        if isinstance(agent_answer, (int, float)):
            agent_avg = float(agent_answer)
        elif isinstance(agent_answer, str):
            # 移除货币符号、逗号和空格，提取数字
            clean_str = agent_answer.replace("¥", "").replace("￥", "").replace(",", "").strip()
            agent_avg = float(clean_str)
        elif isinstance(agent_answer, dict):
            # 从字典中获取可能包含数字的句子（优先final_message，其次avg）
            # 先获取对应键的值，默认空字符串
            agent_value = agent_answer.get("final_message", agent_answer.get("avg", 0))

            # 如果值是字符串，尝试从中提取数字
            if isinstance(agent_value, str):
                # 清理字符串：移除货币符号、逗号等干扰字符
                clean_value = agent_value.replace("¥", "").replace("￥", "").replace(",", "").strip()
                # 用正则提取所有数字（支持整数和小数，如168、168.5）
                numbers = re.findall(r"\d+\.?\d*", clean_value)
                if not numbers:  # 没提取到数字，验证失败
                    return False
                # 取第一个数字作为目标值（默认句子中只有一个价格数字）
                agent_avg = float(numbers[0])
            else:
                # 如果值不是字符串（如直接是数字），尝试直接转换
                agent_avg = float(agent_value)
        else:
            return False  # 不支持的类型

        # 允许±1元的误差（因为可能有四舍五入）
        return abs(agent_avg - expected_avg) <= 1

    except (ValueError, TypeError):
        return False


def check_from_search_params_file(device_id=None, backup_dir=None):
    """
    从search_params.json文件中检查是否记录了正确的搜索参数
    """
    app_package = "com.example.Ctrip"
    phone_file_path = "files/search_params.json"
    local_file_path = os.path.join(backup_dir, 'search_params.json') if backup_dir else 'search_params.json'

    # 1. 通过ADB获取文件内容
    try:
        # 构建adb命令,如果提供了device_id就添加设备选择参数
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", app_package, "cat", phone_file_path])

        with open(local_file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f)

        # 2. 解析JSON内容
        with open(local_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False

    # 3. 检查最新记录是否包含指定字段且显示了列表
    try:
        latest_event = data["search_events"][-1]
        return (
            latest_event.get("type") == "flight_search"
            and latest_event.get("from") == "北京"
            and latest_event.get("to") == "广州"
            and latest_event.get("date") == "2025-10-21"
            and latest_event.get("calculation") == "average_price_top3"
            and latest_event.get("list_shown") == True
        )
    except:
        return False


if __name__ == "__main__":
    # 计算并打印预期答案
    expected_avg, top3_flights = get_expected_average_price_top3()

    print(f"预期答案：10月21日北京到广州最便宜的3趟航班平均价格 = {expected_avg:.2f}元")
    print("\n最便宜的3趟航班：")
    for i, flight in enumerate(top3_flights, 1):
        print(
            f"  {i}. {flight['flightNumber']} ({flight['airline']}) "
            f"{flight['departureTime']}-{flight['arrivalTime']} "
            f"{flight['price']}元 ({flight['cabinClass']})"
        )

    print(
        f"\n计算过程：({top3_flights[0]['price']} + {top3_flights[1]['price']} + {top3_flights[2]['price']}) / 3 = {expected_avg:.2f}元"
    )

    # 如果要从文件检查，使用：
    # file_check_result = check_from_search_params_file()
    # print(f"\n从search_params.json文件检查: {'true' if file_check_result else 'false'}")

    # 如果要验证智能体答案，使用：
    result = check_flight_search_price_avg(agent_answer)
    print("true" if result else "false")
