# Task 10: 在全屏播放页面播放或者暂停歌曲
# Check: Full-screen playing view is open and play/pause button state changed
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Now Playing")
        and (c.find_desc("Pause") or c.find_desc("Play"))
    )


if __name__ == "__main__":
    run_check(check, 10)
