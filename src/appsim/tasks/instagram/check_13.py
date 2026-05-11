"""
Check Script #13: 修改用户名为'Li'、性别改为男性、设为私密账户、开启睡眠模式
Difficulty: 3 (Hard)
Check Method: Read user_state.json for multiple account settings
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    user = get_user_state(adb)
    if not user:
        return result_fail("Unable to read user_state.json")

    checks = {
        "username": user.get("username", "").lower() == "li",
        "private": user.get("isPrivate") is True,
        "sleep_mode": user.get("sleepMode") is True,
    }

    # Gender check
    gender = user.get("gender", "")
    if gender:
        checks["gender"] = gender.lower() == "male"
    else:
        checks["gender"] = ui.has_text("Male") or ui.has_text("male")

    missing = [k for k, v in checks.items() if not v]
    if not missing:
        return result_pass("All account settings updated (username+gender+private+sleep)")
    passed = [k for k, v in checks.items() if v]
    return result_fail(f"Partially completed. Done: {passed}, Missing: {missing}")


if __name__ == "__main__":
    run_check(check)
