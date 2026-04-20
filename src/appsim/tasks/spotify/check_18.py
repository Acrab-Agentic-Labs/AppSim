# Task 18: 查看当前播放歌曲的歌词
# Check: Lyrics view is open
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_desc("Back")
        and c.find_desc("Share")
        and (
            c.find_text_contains("I close my eyes")
            or c.find_text("Lyrics")
        )
    )


if __name__ == "__main__":
    run_check(check, 18)
