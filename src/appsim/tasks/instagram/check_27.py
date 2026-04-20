"""
检测脚本 #27: 随机选择一位用户并拉黑
难度: 2 (中等)
检测方式: 读取 user_state.json 验证 blockedUsers 不为空
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        blocked = user.get("blockedUsers", [])
        if blocked:
            return result_pass(f"已拉黑用户: {blocked} (JSON验证)")
        return result_fail("blockedUsers 为空，未拉黑任何用户")

    # Fallback: UI check
    if ui.has_text("Blocked") and ui.has_text("Unblock"):
        return result_pass("已成功拉黑用户（Blocked列表中有用户）")

    return result_fail("未检测到拉黑操作")


if __name__ == "__main__":
    run_check(check)
