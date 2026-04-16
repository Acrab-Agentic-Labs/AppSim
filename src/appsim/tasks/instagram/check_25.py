"""
检测脚本 #25: 修改username为"zhou"
难度: 2 (中等)
检测方式: 检查 user_state.json 或 UI 中 username 是否为 "zhou"
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        username = user.get("username", "")
        if username.lower() == "zhou":
            return result_pass(f"username 已修改为 '{username}' (JSON验证)")
        return result_fail(f"username 仍为 '{username}'，未修改为 'zhou'")

    # Fallback: UI check
    if ui.has_text("zhou"):
        if ui.has_text("Edit profile") or ui.has_text("Share profile"):
            return result_pass("页面上显示 username 'zhou'")
        return result_pass("检测到 'zhou' 文本")

    if ui.has_text("Edit profile"):
        return result_fail("在编辑资料页面但 username 不是 'zhou'")

    return result_fail("未检测到 username 'zhou'")


if __name__ == "__main__":
    run_check(check)
