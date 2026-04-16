"""
检测脚本 #38: 创建新帖子，隐藏点赞数、开启Facebook分享
难度: 3 (困难)
检测方式: 读取 new_post_events.json 验证设置
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # Primary: check via JSON state
    events = get_new_post_events(adb)
    if events:
        for event in events:
            if event.get("isReel"):
                continue
            hide_likes = event.get("hideLikesAndViews") is True
            fb_share = event.get("shareToFacebook") is True

            missing = []
            if not hide_likes: missing.append("隐藏点赞数")
            if not fb_share: missing.append("Facebook分享")

            if not missing:
                return result_pass("帖子已发布: 点赞数已隐藏+Facebook分享已开启 (JSON验证)")
            if len(missing) < 2:
                return result_fail(f"帖子已发布但缺少: {', '.join(missing)}")

        return result_fail("已有发帖记录但设置不匹配")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("帖子已成功发布")

    return result_fail("未检测到帖子发布结果")


if __name__ == "__main__":
    run_check(check)
