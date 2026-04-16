"""
检测脚本 #26: 关注首页第三个帖子的作者
难度: 2 (中等)
检测方式: 读取 user_state.json 验证 following 列表有增加
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *

# Initial following list (from users.json seed data)
INITIAL_FOLLOWING = ["user_anushka", "user_naina", "user_deepak", "user_yashi"]


def check(adb, ui):
    # Primary: check via JSON state
    user = get_user_state(adb)
    if user:
        current_following = user.get("following", [])
        new_follows = [u for u in current_following if u not in INITIAL_FOLLOWING]
        if new_follows:
            return result_pass(f"新关注了用户: {new_follows} (JSON验证)")
        if len(current_following) > len(INITIAL_FOLLOWING):
            return result_pass(f"关注列表增加到 {len(current_following)} 人 (JSON验证)")
        return result_fail(f"关注列表未变化，仍为 {len(current_following)} 人")

    # Fallback: UI check
    following_nodes = ui.find_by_text("Following")
    if following_nodes:
        return result_pass("已成功关注用户（按钮显示'Following'）")

    return result_fail("未检测到关注成功状态")


if __name__ == "__main__":
    run_check(check)
