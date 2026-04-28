import json
import os
import re
import subprocess

# 任务32：订10月20日从杭州到北京最快火车票（5小时内达），住北京王府井希尔顿酒店两晚（10.20-10.22），再订10.22北京回杭州的火车，计算所有费用后判断2000元够不够
# 检查条件：最后3条记录依次是火车票(杭州->北京, 2025-10-20, 最快且5小时内)、酒店(北京, 王府井希尔顿, 10.20-10.22)、火车票(北京->杭州, 2025-10-22)


def check_booking_complex_budget(agent_answer=None, device_id=None, backup_dir=None):
    if agent_answer is None:
        return False
    final_message = agent_answer.get("final_message")
    if not isinstance(final_message, str):
        return False

    app_package = "com.example.ctrip_sim"
    phone_file_path = "files/booking_history.json"
    local_file_path = os.path.join(backup_dir, "booking_history.json") if backup_dir else "booking_history.json"

    try:
        cmd = ["adb"]
        if device_id:
            cmd.extend(["-s", device_id])
        cmd.extend(["exec-out", "run-as", app_package, "cat", phone_file_path])

        with open(local_file_path, "w", encoding="utf-8") as f:
            subprocess.run(cmd, stdout=f)

        with open(local_file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except subprocess.CalledProcessError:
        return False
    except Exception:
        return False

    try:
        booking_events = data.get("booking_events", [])
        if len(booking_events) < 3:
            return False

        first_train = booking_events[-3]
        hotel_booking = booking_events[-2]
        third_train = booking_events[-1]

        if not (
            first_train.get("type") == "train_booking"
            and first_train.get("from") == "杭州"
            and first_train.get("to") == "北京"
            and first_train.get("date") == "2025-10-20"
        ):
            return False

        duration_str = first_train.get("duration", "")
        hour_match = re.search(r"(\d+)时", duration_str)
        minute_match = re.search(r"(\d+)分", duration_str)
        hours = int(hour_match.group(1)) if hour_match else 0
        minutes = int(minute_match.group(1)) if minute_match else 0
        duration_minutes = hours * 60 + minutes

        # 当前任务里“最快且5小时内”的正确记录应为 4时0分。
        if duration_minutes != 240:
            return False

        if not (
            hotel_booking.get("type") == "hotel_booking"
            and hotel_booking.get("city") == "北京"
            and hotel_booking.get("checkIn") == "2025-10-20"
            and hotel_booking.get("checkOut") == "2025-10-22"
            and "王府井希尔顿" in hotel_booking.get("hotelName", "")
        ):
            return False

        if not (
            third_train.get("type") == "train_booking"
            and third_train.get("from") == "北京"
            and third_train.get("to") == "杭州"
            and third_train.get("date") == "2025-10-22"
        ):
            return False

        if "final_message" in agent_answer and (
            "足够" in agent_answer["final_message"]
            or ("够" in agent_answer["final_message"] and "不够" not in agent_answer["final_message"])
            or ("enough" in agent_answer["final_message"].lower() and "not enough" not in agent_answer["final_message"].lower())
        ):
            return True
        else:
            return False
    except Exception:
        return False


if __name__ == "__main__":
    print("true" if check_booking_complex_budget() else "false")
