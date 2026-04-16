"""
检测脚本 #15: 分享首页第一条帖子
难度: 2 (中等)
检测方式: 检查分享底部弹窗是否打开
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # ShareBottomSheet 包含: Copy link, Add to story, Share to..., QR code
    share_indicators = ["Copy link", "Add to story", "Share to", "QR code"]
    found = sum(1 for indicator in share_indicators if ui.has_text(indicator))

    if found >= 2:
        return result_pass(f"分享弹窗已打开（匹配 {found} 个分享选项）")

    if found >= 1:
        return result_pass("分享弹窗已打开")

    return result_fail("分享弹窗未打开")


if __name__ == "__main__":
    run_check(check)
