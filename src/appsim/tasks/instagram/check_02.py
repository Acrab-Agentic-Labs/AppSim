"""
检测脚本 #2: 告诉我当前播放的短视频有几个点赞
难度: 1 (简单)
检测方式: 检查是否在Reels页面，找到当前短视频的点赞数
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在Reels页面
    descs = ui.get_all_descs()
    reel_indicators = ["Like", "Comment", "Share", "Save"]
    found = sum(1 for i in reel_indicators if i in descs)
    if not ui.has_text("Reels") and found < 2:
        return result_fail("当前不在Reels页面")

    # 查找点赞数: 带 "like" 的 content-desc，如 "1.2K likes"
    for desc in descs:
        if re.match(r'^\d+(\.\d+)?[KMkm]?\s*(likes?)', desc.strip(), re.IGNORECASE):
            return result_pass(f"找到点赞数: {desc}")

    # 查找独立数字文本 (点赞数通常显示在 Like 按钮附近)
    all_texts = ui.get_all_texts()
    for text in all_texts:
        if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
            return result_pass(f"找到短视频互动数据: {text}")

    return result_fail("未找到短视频点赞数")


if __name__ == "__main__":
    run_check(check)
