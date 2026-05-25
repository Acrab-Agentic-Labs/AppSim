"""
Check Script #1: Tell me how many likes the first post on the homepage has
Difficulty: 1 (Easy)
Check Method: Verify if on homepage, find and extract like count from first post, verify answer
"""
import sys, os, re
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def check(adb, ui, result=None):
    # Check if on homepage
    if not ui.has_text("Instagram"):
        return result_fail("Not on homepage")

    # Find like count in format: "123 likes" or "1.2K likes"
    like_count_text = None
    all_texts = ui.get_all_texts()
    for text in all_texts:
        if re.match(r'^\d+(\.\d+)?[KMkm]?\s*(likes?|个赞)', text.strip(), re.IGNORECASE):
            like_count_text = text.strip()
            break

    if not like_count_text:
        # Check content-desc for like count info
        descs = ui.get_all_descs()
        for desc in descs:
            if re.match(r'^\d+(\.\d+)?[KMkm]?\s*(likes?|个赞)', desc.strip(), re.IGNORECASE):
                like_count_text = desc.strip()
                break

    if not like_count_text:
        return result_fail("Like count information not found")

    # Extract the number from like_count_text
    num_match = re.match(r'^(\d+(\.\d+)?[KMkm]?)', like_count_text)
    expected_num = num_match.group(1) if num_match else None

    # Verify the agent's answer via extracted_answer
    if result and isinstance(result, dict):
        extracted_answer = result.get("extracted_answer")
        if isinstance(extracted_answer, dict):
            like_count_val = str(extracted_answer.get("like_count") or "")
            if expected_num and expected_num in like_count_val:
                return result_pass(f"Found like count: {like_count_text}, answer correct")

    return result_fail(f"Answer does not contain correct like count ({expected_num})")


if __name__ == "__main__":
    run_check(check)
