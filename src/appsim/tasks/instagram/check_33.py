"""
检测脚本 #33: 创建一个名为'Favorites'的新收藏夹
难度: 3 (困难)
检测方式: 检查Saved页面是否出现名为'Favorites'的收藏夹
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 检查Saved页面是否有Favorites收藏夹
    if ui.has_text("Favorites"):
        if ui.has_text("Saved"):
            return result_pass("收藏夹'Favorites'已成功创建（在Saved页面中可见）")
        return result_pass("检测到'Favorites'文本")

    # 检查是否在新建收藏夹对话框中
    if ui.has_text("New Collection") or ui.has_text("Collection name"):
        return result_fail("新建收藏夹对话框仍打开，可能未完成创建")

    # 检查是否在Saved页面
    if ui.has_text("Saved"):
        return result_fail("在Saved页面但未找到'Favorites'收藏夹")

    return result_fail("当前不在Saved页面")


if __name__ == "__main__":
    run_check(check)
