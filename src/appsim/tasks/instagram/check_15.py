"""
Check Script #15: 分享首页第一条帖子
Difficulty: 2 (Medium)
Check Method: Check if share bottom sheet opened
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # ShareBottomSheet contains: Copy link, Add to story, Share to..., QR code
    share_indicators = ["Copy link", "Add to story", "Share to", "QR code"]
    found = sum(1 for indicator in share_indicators if ui.has_text(indicator))

    if found >= 2:
        return result_pass(f"Share sheet opened (matched {found} share options)")

    if found >= 1:
        return result_pass("Share sheet opened")

    return result_fail("Share sheet not opened")


if __name__ == "__main__":
    run_check(check)
