# Task 24: 在搜索输入页面删除一条最近搜索记录
# Check: 通过 JSON 验证最近搜索记录恰好删除一条
from .check_common import AppChecker, run_check, result_pass, result_fail


EXPECTED_REMOVED_COUNT = 1


def check(c: AppChecker):
    # Must be on search input page
    if not c.find_text("Cancel"):
        return result_fail("UI check failed: not on search input page")

    if not c.find_text("Recent searches"):
        return result_fail("UI check failed: Recent searches not found")

    state = c.read_json_from_device("search_state.json")
    if not state:
        return result_fail("State check failed: unable to read search_state.json")

    initial_count = state.get("initialCount")
    current_count = state.get("currentCount")
    removed_count = state.get("removedCount")
    removed_items = state.get("removedItems", [])

    if removed_count == EXPECTED_REMOVED_COUNT and current_count == initial_count - EXPECTED_REMOVED_COUNT:
        return result_pass("Check passed: exactly one recent search item was removed")

    return result_fail(
        "State check failed: recent search deletion count is not exactly one",
        {
            "initialCount": initial_count,
            "currentCount": current_count,
            "removedCount": removed_count,
            "removedItems": removed_items,
        },
    )


if __name__ == "__main__":
    run_check(check, 24)
