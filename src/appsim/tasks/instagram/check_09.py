"""
检测脚本 #9: 转发第一个帖子
难度: 1 (简单)
检测方式: 检查是否出现转发成功提示（Reposted toast）
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 转发操作后应该出现 "Reposted" toast/snackbar
    if ui.has_text("Reposted"):
        return result_pass("帖子已成功转发（Reposted提示已出现）")

    # 检查是否在首页且转发按钮存在（备选检查）
    if ui.has_text("Instagram"):
        descs = ui.get_all_descs()
        if "Repost" in descs:
            return result_fail("转发按钮存在但未检测到转发成功提示")

    return result_fail("未检测到转发成功状态")


if __name__ == "__main__":
    run_check(check)
