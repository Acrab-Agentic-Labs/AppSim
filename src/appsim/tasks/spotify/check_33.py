# Task 33: 进行会员付费操作
# Check: Checkout page is visible with payment options
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Checkout")
        and c.find_text("Premium Individual")
        and (
            c.find_text("Payment method")
            or c.find_text("Activate Premium")
        )
    )


if __name__ == "__main__":
    run_check(check, 33)
