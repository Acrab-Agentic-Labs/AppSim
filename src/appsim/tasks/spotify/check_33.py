# Task 33: 进行会员付费操作
# Check: Checkout page is visible with payment options
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    passed = (
        c.find_text("Checkout")
        and c.find_text("Premium Individual")
        and (
            c.find_text("Payment method")
            or c.find_text("Activate Premium")
        )
    )
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 33)
