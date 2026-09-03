"""
Check Script #18: 查看个人粉丝数量
Difficulty: 2 (Medium)
Check Method: Check if on Profile page showing follower count, verify answer
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_follower_count(adb, ui, result=None):
    follower_count = None

    # Check if on Profile page
    if ui.has_text("Followers") and ui.has_text("Following"):
        all_texts = ui.get_all_texts()
        for text in all_texts:
            if "Followers" in text and any(c.isdigit() for c in text):
                num_match = re.search(r'(\d+(\.\d+)?[KMkm]?)', text)
                if num_match:
                    follower_count = num_match.group(1)
                break
        if not follower_count:
            for text in all_texts:
                if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
                    follower_count = text.strip()
                    break

    if not follower_count and ui.has_text("Edit profile"):
        if ui.has_text("Followers"):
            all_texts = ui.get_all_texts()
            for text in all_texts:
                if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
                    follower_count = text.strip()
                    break

    if not follower_count:
        return result_fail("Follower count information not found")

    if result and isinstance(result, dict):
        extracted_answer = result.get("extracted_answer")
        if isinstance(extracted_answer, dict):
            fc_val = str(extracted_answer.get("follower_count") or "")
            if follower_count in fc_val:
                return result_pass(f"Found follower count: {follower_count}, answer correct")

    return result_fail(f"Answer does not contain follower count ({follower_count})")


if __name__ == "__main__":
    run_check(verify_follower_count)
