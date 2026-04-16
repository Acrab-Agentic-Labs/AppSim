"""
检测脚本 #28: 随机添加一位亲密好友
难度: 2 (中等)
检测方式: 读取 user_state.json 验证 closeFriends 不为空
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        close_friends = user.get("closeFriends", [])
        if close_friends:
            return result_pass(f"已添加亲密好友: {close_friends} (JSON验证)")
        return result_fail("closeFriends 为空，未添加任何亲密好友")

    # Fallback: UI check
    if ui.has_text("Close friends") and ui.has_text("Remove"):
        return result_pass("已成功添加亲密好友（显示Remove按钮）")

    return result_fail("未检测到亲密好友添加操作")


if __name__ == "__main__":
    run_check(check)
