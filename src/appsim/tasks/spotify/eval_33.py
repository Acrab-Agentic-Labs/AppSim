# Task 33: 进行会员付费操作
# Check: 通过 JSON 验证 premium 状态已激活
from .check_common import AppChecker, run_check, result_pass, result_fail


def verify_premium_subscription_activated(c: AppChecker):
    state = c.read_json_from_device("premium_state.json")
    if not state:
        return result_fail("Check failed: unable to read premium_state.json")

    is_premium = state.get("isPremium")
    subscription_date = state.get("subscriptionDate")

    if is_premium is True and subscription_date:
        return result_pass("Check passed: Premium subscription activated")

    return result_fail(
        "Check failed: Premium subscription not activated",
        {"isPremium": is_premium, "subscriptionDate": subscription_date},
    )


if __name__ == "__main__":
    run_check(verify_premium_subscription_activated, 33)
