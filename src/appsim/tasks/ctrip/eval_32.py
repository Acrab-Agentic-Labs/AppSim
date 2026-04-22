import json
import subprocess
import sys
import os

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


def check_booking_complex_budget(result=None, device_id=None, backup_dir=None):
    """
    检查复杂预订任务（含预算判断）

    Args:
        agent_answer: 智能体的答案，应为"enough"或"not_enough"
        device_id: 设备ID（可选）
    """
    agent_answer = result

    app_package = "com.example.ctrip_sim"
    phone_file_path = "files/booking_history.json"
    local_file_path = os.path.join(backup_dir, 'booking_history.json') if backup_dir else 'booking_history.json'

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
        # 新增：精准匹配目标入住和退房日期
        target_check_in = "2025-10-20"
        target_check_out = "2025-10-22"
        if check_in != target_check_in or check_out != target_check_out:
            return False



        # 验证第3步：火车票(北京->杭州)
        step3 = last_three[2]
        if not (step3.get("type") == "train_booking" and step3.get("from") == "北京" and step3.get("to") == "杭州"):
            return False



        # 智能体答案，进行对比
        if agent_answer is None:
            return False
        final_message = agent_answer.get("final_message")
        if not isinstance(final_message, str):
            return False
        # 检测 result 中的final_messages中是否包含 "够"或者'enough'
        if ('final_message' in agent_answer and (
                '不够' not in agent_answer['final_message'] or
                'not enough' not in agent_answer['final_message'])
        ):
            return True
        else:
            return False

    except Exception as e:
        return False


if __name__ == "__main__":
    print(check_booking_complex_budget())
