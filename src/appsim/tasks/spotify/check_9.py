# Task 9: 告诉我当前正在播放歌曲的歌手是谁
# Check: Full-screen playing view or mini player is visible showing artist info
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # Prefer full-screen playing view where artist is clearly visible
    return (
        c.find_text("Now Playing")
        and c.find_desc("Album Cover")
    ) or (
        c.find_desc("Now Playing Cover")
    )


if __name__ == "__main__":
    run_check(check, 9)
