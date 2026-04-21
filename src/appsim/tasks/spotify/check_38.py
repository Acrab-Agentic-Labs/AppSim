# Task 38: 创建一个新的歌单并添加两首新的歌曲
# Check: 通过 JSON 验证 user_playlists 中存在新歌单且其 songIds 包含至少 2 首歌
# Fallback: UI 上出现 "Added" 相关提示
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    # 优先使用 JSON 验证
    playlists = c.get_user_playlists()
    if playlists and isinstance(playlists, list):
        for p in playlists:
            song_ids = p.get("songIds", [])
            # 找到一个有至少 2 首歌的用户歌单
            if len(song_ids) >= 2:
                return result_pass("Playlist with 2+ songs found")

    # Fallback: UI 验证
    passed = c.find_desc("Added") or c.find_text("Added to playlist")
    return result_pass("Check passed") if passed else result_fail("Check failed")


if __name__ == "__main__":
    run_check(check, 38)
