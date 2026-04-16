# Task 11: 播放下一首歌曲
# Check: Full-screen playing view is open (next song was played)
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_text("Now Playing")
        and c.find_desc("Album Cover")
        and c.find_desc("Next")
    )


if __name__ == "__main__":
    run_check(check, 11)
