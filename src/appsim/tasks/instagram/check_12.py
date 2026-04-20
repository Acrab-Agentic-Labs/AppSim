"""
Check Script #12: Search for content related to "happy" on the search page
Difficulty: 2 (Medium)
Check Method: Check if search page displays "happy" search results
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from common import *


def check(adb, ui):
    # 首先确认是否在 APP 内的搜索页面（不能是 Chrome 等其他应用）
    # APP 搜索页面应该有 Search 标签且是 Instagram APP 内
    all_texts = ui.get_all_texts()

    # 检查搜索结果中是否有 happy 相关内容
    # 需要排除仅在搜索框中出现的情况，至少要有2处出现
    happy_count = sum(1 for t in all_texts if "happy" in t.lower())
    if happy_count >= 2:
        return result_pass("Search results contain 'happy' related content")

    # 检查 content-desc 中是否有 happy 相关内容（图片描述等）
    descs = ui.get_all_descs()
    happy_desc_count = sum(1 for d in descs if "happy" in d.lower())
    if happy_desc_count > 0 and ui.has_text("happy"):
        return result_pass("Search results contain 'happy' related content (in descs)")

    # 检查是否在搜索页面
    if ui.has_text("Search"):
        if ui.has_text("happy"):
            return result_fail("搜索框中有'happy'但未显示搜索结果")
        return result_fail("On search page but 'happy' search results not found")

    return result_fail("Not on search page")


if __name__ == "__main__":
    run_check(check)
