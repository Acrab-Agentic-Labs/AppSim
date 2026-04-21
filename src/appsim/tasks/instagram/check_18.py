"""
Check Script #18: 查看个人粉丝数量
Difficulty: 2 (Medium)
Check Method: Check if on Followers/Following or Profile page showing follower count
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui):
    # Check if on Profile page（含Followers/Following信息）
    if ui.has_text("Followers") and ui.has_text("Following"):
        all_texts = ui.get_all_texts()

        # Find "123 Followers" 或紧跟 Followers 的数字
        for text in all_texts:
            if "Followers" in text and any(c.isdigit() for c in text):
                return result_pass(f"Found follower count: {text}")

        # Find独立数字（可能是粉丝数）
        for text in all_texts:
            if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
                return result_pass(f"Found number (follower count): {text}")

        # On Profile page with Followers label but no specific number found
        return result_fail("See Followers label but no specific number found")

    # Check if on Profile page
    if ui.has_text("Edit profile"):
        if ui.has_text("Followers"):
            # Profile page has Followers label
            all_texts = ui.get_all_texts()
            for text in all_texts:
                if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
                    return result_pass(f"在个人主页Found follower count: {text}")
            return result_fail("On profile but follower count not found")

    return result_fail("Follower count information not found")


if __name__ == "__main__":
    run_check(check)
