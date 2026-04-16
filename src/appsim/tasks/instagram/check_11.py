"""
检测脚本 #11: 编辑个人主页性别为female
难度: 2 (中等)
检测方式: 检查Edit Profile页面Gender字段是否为Female
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查是否在编辑资料页面
    if ui.has_text("Edit profile"):
        # 检查Gender字段是否设置为Female
        if ui.has_text("Female") or ui.has_text("female"):
            return result_pass("性别已成功设置为Female")

        # 检查Gender字段是否存在
        if ui.has_text("Gender"):
            return result_fail("Gender字段存在但未设置为Female")

        return result_fail("在编辑资料页面但未找到Gender字段")

    return result_fail("当前不在编辑资料页面")


if __name__ == "__main__":
    run_check(check)
