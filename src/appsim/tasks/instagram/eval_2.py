"""
Check Script #2: Tell me how many likes the currently playing short video has
Difficulty: 1 (Easy)
Check Method: Verify if on Reels page, find like count of current reel, verify answer
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_current_reel_like_count(adb, ui, result=None):
    # Check if on Reels page
    descs = ui.get_all_descs()
    reel_indicators = ["Like", "Comment", "Share", "Save"]
    found = sum(1 for i in reel_indicators if i in descs)
    if not ui.has_text("Reels") and found < 2:
        return result_fail("Not on Reels page")

    like_count_text = None

    # Find like count: content-desc with "like", e.g. "1.2K likes"
    for desc in descs:
        if re.match(r'^\d+(\.\d+)?[KMkm]?\s*(likes?)', desc.strip(), re.IGNORECASE):
            like_count_text = desc.strip()
            break

    if not like_count_text:
        # Find standalone number text
        all_texts = ui.get_all_texts()
        for text in all_texts:
            if re.match(r'^\d+(\.\d+)?[KMkm]?$', text.strip()):
                like_count_text = text.strip()
                break

    if not like_count_text:
        return result_fail("Like count not found on reel")

    num_match = re.match(r'^(\d+(\.\d+)?[KMkm]?)', like_count_text)
    expected_num = num_match.group(1) if num_match else None

    if result and isinstance(result, dict):
        extracted_answer = result.get("extracted_answer")
        if isinstance(extracted_answer, dict):
            like_count_val = str(extracted_answer.get("like_count") or "")
            if expected_num and expected_num in like_count_val:
                return result_pass(f"Found like count: {like_count_text}, answer correct")

    return result_fail(f"Answer does not contain correct like count ({expected_num})")


if __name__ == "__main__":
    run_check(verify_current_reel_like_count)
