"""
Check Script #11: 编辑个人主页性别为female
Difficulty: 2 (Medium)
Check Method: Check if Gender field on Edit Profile page is Female
"""
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from .common import *


def verify_profile_gender_updated(adb, ui):
    # Check if on 编辑资料 page
    if ui.has_text("Edit profile"):
        # Check if Gender field set to Female
        if ui.has_text("Female") or ui.has_text("female"):
            return result_pass("Gender successfully set to Female")

        # Check if Gender field exists
        if ui.has_text("Gender"):
            return result_fail("Gender field exists but not set to Female")

        return result_fail("On Edit Profile page but Gender field not found")

    return result_fail("Not on Edit Profile page")


if __name__ == "__main__":
    run_check(verify_profile_gender_updated)
