# Task 25: 在音乐库中创建一个名为'My Rock'的新歌单
# Check: 通过 JSON 验证 user_playlists 中存在名为 "My Rock" 的歌单
# Fallback: UI 上出现 "My Rock" 文本
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    # 优先使用 JSON 验证
    playlists = c.get_user_playlists()
    if playlists and isinstance(playlists, list):
        for p in playlists:
            if p.get("name") == "My Rock":
                return result_pass("Playlist 'My Rock' found")

    # Fallback: UI 验证
    passed = c.find_text("My Rock")
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 25)
