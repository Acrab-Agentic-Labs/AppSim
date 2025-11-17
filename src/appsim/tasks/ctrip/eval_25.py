import json
import os
import re
import subprocess

# 任务25：进入 "火车票" 页面，查10月22日广州到杭州下午2点到5点的车次，检索这些车次中最高的价格
# 检查条件：智能体返回的价格是否是这些车次中的最高价格


# 需要从trains_list.json文件中读取真实数据
def load_train_data():
    """
    加载火车票数据
    """
    try:
        train_data_path = os.path.join(
            os.path.dirname(__file__), "..", "app", "src", "main", "assets", "data", "trains_list.json"
        )
        with open(train_data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading train data: {e}")
        # 如果无法读取文件，使用硬编码的测试数据
        return get_hardcoded_train_data()


def get_hardcoded_train_data():
    """
    硬编码的广州到杭州10月22日的火车票数据
    （从trains_list.json中提取）
    """
    return [
        {
            "trainId": "train_gz_hz_001",
            "trainNumber": "G531",
            "departureCity": "广州",
            "arrivalCity": "杭州",
            "departureDate": "2025-10-22",
            "departureTime": "06:00",
            "arrivalTime": "10:30",
            "prices": {"二等座": 553.5, "一等座": 884.5, "商务座": 1665.5},
        },
        {
            "trainId": "train_gz_hz_002",
            "trainNumber": "D532",
            "departureCity": "广州",
            "arrivalCity": "杭州",
            "departureDate": "2025-10-22",
            "departureTime": "08:15",
            "arrivalTime": "13:05",
            "prices": {"二等座": 489.0, "一等座": 782.5, "商务座": 1471.5},
        },
        {
            "trainId": "train_gz_hz_003",
            "trainNumber": "C533",
            "departureCity": "广州",
            "arrivalCity": "杭州",
            "departureDate": "2025-10-22",
            "departureTime": "10:30",
            "arrivalTime": "15:40",
            "prices": {"二等座": 424.5, "一等座": 680.5},
        },
        {
            "trainId": "train_gz_hz_004",
            "trainNumber": "T534",
            "departureCity": "广州",
            "arrivalCity": "杭州",
            "departureDate": "2025-10-22",
            "departureTime": "12:45",
            "arrivalTime": "18:15",
            "prices": {"硬座": 163.5, "硬卧": 280.5, "软卧": 432.5},
        },
        {
            "trainId": "train_gz_hz_005",
            "trainNumber": "K535",
            "departureCity": "广州",
            "arrivalCity": "杭州",
            "departureDate": "2025-10-22",
            "departureTime": "14:00",
            "arrivalTime": "19:50",
            "prices": {"硬座": 152.5, "硬卧": 261.5, "软卧": 402.5},
        },
    ]


def parse_time(time_str):
    """
    将时间字符串转换为分钟数（方便比较）
    """
    hour, minute = map(int, time_str.split(":"))
    return hour * 60 + minute


def get_trains_in_time_range():
    """
    获取10月22日广州到杭州下午2点到5点（14:00-17:00）的车次
    """
    # 加载所有火车票数据
    all_trains = load_train_data()

    # 筛选广州到杭州10月22日的火车
    gz_hz_trains = [
        train
        for train in all_trains
        if train.get("departureCity") == "广州"
        and train.get("arrivalCity") == "杭州"
        and train.get("departureDate") == "2025-10-22"
    ]

    # 筛选下午2点到5点（14:00-17:00）出发的车次
    afternoon_trains = []
    for train in gz_hz_trains:
        dept_time_minutes = parse_time(train["departureTime"])
        # 14:00 = 14*60 = 840分钟
        # 17:00 = 17*60 = 1020分钟
        if 840 <= dept_time_minutes < 1020:
            afternoon_trains.append(train)

    return afternoon_trains


def get_expected_max_price():
    """
    计算真实答案：这些车次中最高的价格
    """
    # 获取符合时间条件的车次
    trains = get_trains_in_time_range()

    if not trains:
        return None, []

    # 找出所有车次中的所有价格
    all_prices = []
    for train in trains:
        prices = train.get("prices", {})
        for seat_type, price in prices.items():
            all_prices.append({"train": train["trainNumber"], "seat_type": seat_type, "price": price})

    # 找出最高价格
    if all_prices:
        max_price_info = max(all_prices, key=lambda x: x["price"])
        return max_price_info["price"], trains

    return None, trains


def check_train_search_max_price(result=None, device_id=None):
    """
    检验函数：验证智能体答案是否正确

    参数:
        agent_answer: 智能体生成的答案，可以是：
                     - 数字: 402.5 或 402
                     - 字符串: "402.5" 或 "¥402.5"
                     - 包含价格的字典: {"price": 402.5, "max_price": 402.5}

    返回:
        True: 验证成功（允许±1元的误差）
        False: 验证失败
    """
    agent_answer = result
    # 计算真实答案
    expected_price, _ = get_expected_max_price()

    if expected_price is None:
        return False

    # 处理不同类型的智能体答案
    try:
        if isinstance(agent_answer, (int, float)):
            agent_price = float(agent_answer)
        elif isinstance(agent_answer, str):
            # 移除货币符号、逗号和空格，提取数字
            clean_str = agent_answer.replace("¥", "").replace("￥", "").replace(",", "").strip()
            agent_price = float(clean_str)
        elif isinstance(agent_answer, dict):
            # 从字典中获取可能包含数字的句子（优先final_message，其次avg）
            # 先获取对应键的值，默认空字符串
            agent_value = agent_answer.get("final_message", agent_answer.get(0))

            # 如果值是字符串，尝试从中提取数字
            if isinstance(agent_value, str):
                # 清理字符串：移除货币符号、逗号等干扰字符
                clean_value = agent_value.replace("¥", "").replace("￥", "").replace(",", "").strip()
                # 用正则提取所有数字（支持整数和小数，如168、168.5）
                numbers = re.findall(r"\d+\.?\d*", clean_value)
                if not numbers:  # 没提取到数字，验证失败
                    return False
                # 取第一个数字作为目标值（默认句子中只有一个价格数字）
                agent_price = float(numbers[0])
            else:
                # 如果值不是字符串（如直接是数字），尝试直接转换
                agent_price = float(agent_value)
        else:
            return False  # 不支持的类型

        # 允许±1元的误差
        return abs(agent_price - expected_price) <= 1

    except (ValueError, TypeError):
        return False


def check_from_search_params_file(device_id=None):
    """
    从search_params.json文件中检查是否记录了正确的搜索参数
    """
    app_package = "com.example.Ctrip"
    phone_file_path = "files/search_params.json"

    # 1. 通过ADB获取文件内容
    try:
        # 构建adb命令,如果提供了device_id就添加设备选择参数
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", app_package, "cat", phone_file_path])

        result = subprocess.run(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding="utf-8", check=True
        )
        file_content = result.stdout
    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False

    # 2. 解析JSON内容
    try:
        data = json.loads(file_content)
    except json.JSONDecodeError:
        return False
    except Exception:
        return False

    # 3. 检查最新记录是否包含指定字段且显示了列表
    try:
        latest_event = data["search_events"][-1]
        return (
            latest_event.get("type") == "train_search"
            and latest_event.get("from") == "广州"
            and latest_event.get("to") == "杭州"
            and latest_event.get("date") == "2025-10-22"
            and latest_event.get("timeRange") == "14:00-17:00"
            and latest_event.get("calculation") == "max_price"
            and latest_event.get("list_shown") == True
        )
    except:
        return False


if __name__ == "__main__":
    # 计算并打印预期答案
    expected_price, trains = get_expected_max_price()

    print(f"预期答案：10月22日广州到杭州下午2点到5点车次中最高的价格 = {expected_price}元")

    print(f"\n符合时间条件的车次共{len(trains)}趟：")
    for train in trains:
        print(f"\n  {train['trainNumber']} {train['departureTime']}-{train['arrivalTime']}")
        prices = train.get("prices", {})
        for seat_type, price in prices.items():
            print(f"    {seat_type}: {price}元")

    # 如果要从文件检查，使用：
    # file_check_result = check_from_search_params_file()
    # print(f"\n从search_params.json文件检查: {'true' if file_check_result else 'false'}")

    # 如果要验证智能体答案，使用：
    result = check_train_search_max_price(agent_answer)
    print("true" if result else "false")
