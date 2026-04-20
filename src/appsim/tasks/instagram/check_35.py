"""
检测脚本 #35: 创建新帖子：含投票 'Which is better?' + 'Option A'/'Option B'
难度: 3 (困难)
检测方式: 读取 new_post_events.json 验证帖子已发布
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state — 验证有帖子被发布
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if not event.get("isReel"):
                return result_pass("帖子已发布 (JSON验证)")
        return result_fail("只有Reel记录，没有Post记录")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("含投票的帖子已成功发布")

    if ui.has_text("Instagram"):
        if ui.has_text("Which is better?") or ui.has_text("Option A") or ui.has_text("Option B"):
            return result_pass("帖子已发布，包含投票内容")
        return result_fail("已返回首页，但未找到投票内容")

    return result_fail("未检测到帖子发布结果")


if __name__ == "__main__":
    run_check(check)
