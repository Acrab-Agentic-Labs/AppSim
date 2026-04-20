"""
检测脚本 #34: 创建新帖子：选第二张图片，标题'Beautiful sunset'，#nature，位置'Central Park'
难度: 3 (困难)
检测方式: 读取 new_post_events.json 验证帖子参数
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
            has_caption = "Beautiful sunset" in (event.get("caption") or "")
            has_hashtag = "nature" in (event.get("hashtags") or [])
            has_location = event.get("location") == "Central Park"

            missing = []
            if not has_caption: missing.append("标题")
            if not has_hashtag: missing.append("#nature标签")
            if not has_location: missing.append("位置")

            if not missing:
                return result_pass("帖子已发布，包含所有要求内容 (JSON验证)")
            if len(missing) < 3:
                return result_fail(f"帖子已发布但缺少: {', '.join(missing)}")

        return result_fail("已有发帖记录但内容不匹配")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("帖子已成功发布（Post shared提示）")

    if ui.has_text("Instagram"):
        if ui.has_text("Beautiful sunset") or ui.has_text("#nature") or ui.has_text("Central Park"):
            return result_pass("帖子已发布（在首页找到帖子内容）")
        return result_fail("已返回首页，但未找到帖子内容")

    return result_fail("未检测到帖子发布结果")


if __name__ == "__main__":
    run_check(check)
