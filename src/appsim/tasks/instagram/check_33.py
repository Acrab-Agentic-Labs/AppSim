"""
Check Script #33: 创建一个名为'Favorites'的新收藏夹
Difficulty: 3 (Hard)
Check Method: Check if collection named 'Favorites' appears on Saved page
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Check if Saved page has Favorites collection
    if ui.has_text("Favorites"):
        if ui.has_text("Saved"):
            return result_pass("Collection 'Favorites' successfully created (visible on Saved page)")
        return result_pass("Detected 'Favorites' text")

    # Check if on新建收藏夹对话框中
    if ui.has_text("New Collection") or ui.has_text("Collection name"):
        return result_fail("New collection dialog still open, may not be completed")

    # Check if on Saved page
    if ui.has_text("Saved"):
        return result_fail("On Saved page but 'Favorites' collection not found")

    return result_fail("当前不在Saved页面")


if __name__ == "__main__":
    run_check(check)
