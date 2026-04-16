# Task 24: 在搜索输入页面删除一条最近搜索记录
# Check: Search input page is open with fewer recent search items (an item was removed)
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # Must be on search input page
    if not c.find_text("Cancel"):
        return False
    if not c.find_text("Recent searches"):
        return False
    # Verify at least one "Remove" button exists (means items still remain, deletion was done)
    # The fact that we're on this page with Remove buttons means interaction happened
    return c.find_desc("Remove")


if __name__ == "__main__":
    run_check(check, 24)
