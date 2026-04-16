"""
检测脚本 #39: 创建新帖子：标题+标签+位置+隐藏点赞+关闭评论
难度: 3 (困难)
检测方式: 读取 new_post_events.json 验证所有设置
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if event.get("isReel"):
                continue
            checks = {
                "标题": "Beautiful sunset" in (event.get("caption") or ""),
                "#nature标签": "nature" in (event.get("hashtags") or []),
                "位置": event.get("location") == "Central Park",
                "隐藏点赞": event.get("hideLikesAndViews") is True,
                "关闭评论": event.get("turnOffComments") is True,
            }
            missing = [k for k, v in checks.items() if not v]

            if not missing:
                return result_pass("帖子已发布，包含所有要求设置 (JSON验证)")
            if len(missing) < len(checks):
                passed = [k for k, v in checks.items() if v]
                return result_fail(f"帖子已发布，已完成: {passed}，缺少: {missing}")

        return result_fail("已有发帖记录但内容不匹配")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("帖子已成功发布")

    if ui.has_text("Instagram"):
        if ui.has_text("Beautiful sunset") or ui.has_text("Central Park"):
            return result_pass("帖子已发布，在首页找到帖子内容")
        return result_fail("已返回首页，但未找到帖子内容")

    return result_fail("未检测到帖子发布结果")


if __name__ == "__main__":
    run_check(check)
