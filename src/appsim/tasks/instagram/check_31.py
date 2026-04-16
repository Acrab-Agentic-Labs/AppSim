"""
检测脚本 #31: 查看个人主页的第一条视频
难度: 3 (困难)
检测方式: 检查是否进入了视频播放页面
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    descs = ui.get_all_descs()

    # 视频播放页面应有 Like/Comment/Share 等按钮，且有 Back 返回
    reel_indicators = ["Like", "Comment", "Share", "Save"]
    found = sum(1 for i in reel_indicators if i in descs)
    has_back = "Back" in descs

    if found >= 3 and has_back:
        return result_pass("已打开视频播放页面")

    # 仍在个人主页上（未点击视频）
    if ui.has_text("Edit profile") or ui.has_text("Share profile"):
        if "Reels" in descs or ui.has_text("Reels"):
            return result_fail("在个人主页Reels标签页，但未打开具体视频")
        return result_fail("在个人主页，但未进入视频播放")

    # 有Back且有部分视频指标
    if has_back and found >= 2:
        return result_pass("在视频播放/详情页面")

    return result_fail("未检测到视频播放页面")


if __name__ == "__main__":
    run_check(check)
