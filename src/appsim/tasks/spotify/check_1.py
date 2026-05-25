# Task 1: 查看当前用户名称
# Check: User profile page is open, username "User" is visible, answer contains username
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    passed = (
        c.find_text("View profile")
        and c.find_text("User")
        and c.find_text("Settings and privacy")
    )
    if not passed:
        return result_fail("Check failed: not on profile page or username not visible")

    if result and isinstance(result, dict):
        extracted_answer = result.get("extracted_answer")
        if isinstance(extracted_answer, dict):
            username_val = str(extracted_answer.get("username") or "")
            if "User" in username_val:
                return result_pass("Check passed: on profile page and answer contains username")

    return result_fail("Check failed: answer does not contain the username 'User'")


if __name__ == "__main__":
    run_check(check, 1)
