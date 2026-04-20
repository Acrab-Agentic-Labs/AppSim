# Task 26: 打开Liked Songs歌单
# Check: Liked Songs page is open
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Liked Songs")
        and c.find_desc("Back")
        and (
            c.find_desc("Shuffle")
            or c.find_desc("Play")
        )
    )


if __name__ == "__main__":
    run_check(check, 26)
