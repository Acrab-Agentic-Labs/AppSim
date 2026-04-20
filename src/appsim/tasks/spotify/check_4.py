# Task 4: 数一下to get you started的第一个推荐歌单有多少首音乐
# Check: Agent opened the first recommended playlist from "To get you started" section
# The first playlist card should be an artist Mix album detail view
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # Agent should have navigated into a playlist detail from "To get you started"
    return (
        c.find_desc("Back")
        and (
            c.find_text_contains("Mix")
            or c.find_desc("Play")
            or c.find_desc("Shuffle")
        )
    )


if __name__ == "__main__":
    run_check(check, 4)
