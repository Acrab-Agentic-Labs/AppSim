import json
import subprocess
import sys

# 任务32：订10月20日从杭州到北京最快火车票（5小时内到达），住北京王府井希尔顿酒店两晚（10.20-10.22），再订10.22北京回杭州的高铁，最后分析计算所有花费后判断2000元够不够
# 检查条件：最后3条记录依次是：火车票(杭州->北京,5小时内)、酒店(北京,王府井希尔顿,2晚)、火车票(北京->杭州)
# 计算总价格，判断2000元是否足够，并与智能体答案对比


def parse_duration(duration_str):
    """
    解析时长字符串，如 "4时55分" -> 295分钟
    """
    import re

    hour_match = re.search(r"(\d+)时", duration_str)
    minute_match = re.search(r"(\d+)分", duration_str)

    hours = int(hour_match.group(1)) if hour_match else 0
    minutes = int(minute_match.group(1)) if minute_match else 0

    return hours * 60 + minutes


def check_booking_complex_budget(result=None, device_id=None):
    """
    检查复杂预订任务（含预算判断）

    Args:
        agent_answer: 智能体的答案，应为"enough"或"not_enough"
        device_id: 设备ID（可选）
    """
    agent_answer = result

    app_package = "com.example.Ctrip"
    phone_file_path = "files/booking_history.json"

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

    # 3. 检查最后3条预订记录
    try:
        booking_events = data.get("booking_events", [])
        if len(booking_events) < 3:
            return False

        # 获取最后3条记录
        last_three = booking_events[-3:]

        # 验证第1步：火车票(杭州->北京)，且5小时内到达
        step1 = last_three[0]
        if not (step1.get("type") == "train_booking" and step1.get("from") == "杭州" and step1.get("to") == "北京"):
            return False

        # 检查时长是否5小时内
        duration1 = step1.get("duration", "")
        if duration1:
            duration_minutes = parse_duration(duration1)
            if duration_minutes > 300:  # 5小时 = 300分钟
                return False
        else:
            return False  # 没有时长信息，返回false

        price1 = step1.get("price", 0)

        # 验证第2步：酒店(北京,包含"王府井"和"希尔顿")
        step2 = last_three[1]
        hotel_name = step2.get("hotelName", "")
        if not (
            step2.get("type") == "hotel_booking"
            and step2.get("city") == "北京"
            and "王府井" in hotel_name
            and "希尔顿" in hotel_name
        ):
            return False

        # 检查是否是2晚（10.20-10.22）
        check_in = step2.get("checkIn", "")
        check_out = step2.get("checkOut", "")
        # 简化检查：只要有入住和退房日期即可，实际应该检查日期差是否为2
        if not (check_in and check_out):
            return False

        price2 = step2.get("price", 0)

        # 验证第3步：火车票(北京->杭州)
        step3 = last_three[2]
        if not (step3.get("type") == "train_booking" and step3.get("from") == "北京" and step3.get("to") == "杭州"):
            return False

        price3 = step3.get("price", 0)

        # 计算总价格
        total_price = price1 + price2 + price3

        # 判断2000元是否足够
        budget_sufficient = total_price <= 2000

        # 智能体答案，进行对比
        if agent_answer is None:
            print("错误: 未提供智能体答案")
            return False
        else:
            # 从字典中获取 final_message
            if isinstance(agent_answer, dict):
                final_message = agent_answer.get("final_message", "")
            else:
                final_message = str(agent_answer)

            # 检查 final_message 中是否包含"够"或"不够"
            agent_says_enough = None
            if "不够" in final_message:
                agent_says_enough = False
            elif "够" in final_message:
                agent_says_enough = True
            else:
                print(f"智能体答案格式错误: 无法从 final_message 中找到'够'或'不够', final_message={final_message}")
                return False

            # 对比智能体判断和实际结果
            if agent_says_enough != budget_sufficient:
                print(
                    f"智能体答案不正确: 实际总价={total_price}元, 预算2000元{'足够' if budget_sufficient else '不够'}, 智能体判断={'够' if agent_says_enough else '不够'}"
                )
                return False

        # 输出调试信息
        print(
            f"预订完成: 火车票1={price1}元, 酒店={price2}元, 火车票2={price3}元, 总计={total_price}元, 2000元{'足够' if budget_sufficient else '不够'}"
        )

        return True
    except Exception as e:
        print(f"检查失败: {e}")
        return False


if __name__ == "__main__":
    # 从命令行参数获取智能体答案（如果有）
    agent_answer = None
    if len(sys.argv) > 1:
        agent_answer = sys.argv[1]

    print("true" if check_booking_complex_budget(agent_answer) else "false")
