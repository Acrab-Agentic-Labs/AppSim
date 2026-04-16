"""
检测脚本 #7: 打开通知页面
难度: 1 (简单)
检测方式: 检查当前是否在Notifications页面
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在通知页面
    if ui.has_text("Notifications"):
        # 进一步确认页面特征
        if ui.has_text("Follow requests") or ui.has_text("This month") or ui.has_text("Earlier"):
            return result_pass("已成功打开通知页面（含完整通知内容）")
        return result_pass("已成功打开通知页面")

    return result_fail("当前不在通知页面")


if __name__ == "__main__":
    run_check(check)
