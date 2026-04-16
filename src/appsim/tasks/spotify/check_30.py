# Task 30: 在首页随机添加一个歌单到音乐库
# Check: Playlist was added to library - "Remove from Library" or snackbar visible
from check_common import AppChecker, run_check


def check(c: AppChecker):
    return (
        c.find_desc("Remove from Library")
        or c.find_text("Added to Your Library")
        or c.find_text("Remove from Library")
    )


if __name__ == "__main__":
    run_check(check, 30)
