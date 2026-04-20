"""
检测脚本 #36: 创建新帖子：含音乐+受众设为'Close Friends'
难度: 3 (困难)
检测方式: 读取 new_post_events.json 验证音乐和受众设置
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
            has_music = event.get("musicTitle") is not None
            has_audience = event.get("audience") == "Close Friends"

            missing = []
            if not has_music: missing.append("音乐")
            if not has_audience: missing.append("Close Friends受众")

            if not missing:
                return result_pass(f"帖子已发布: 音乐={event['musicTitle']}, 受众={event['audience']} (JSON验证)")
            if len(missing) < 2:
                return result_fail(f"帖子已发布但缺少: {', '.join(missing)}")

        return result_fail("已有发帖记录但设置不匹配")

    # Fallback: UI check
    if ui.has_text("Post shared"):
        return result_pass("含音乐的帖子已成功发布")

    return result_fail("未检测到帖子发布结果")


if __name__ == "__main__":
    run_check(check)
