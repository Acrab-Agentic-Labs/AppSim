# Task 32: 在音乐库中除Liked Songs歌单外的其他任一歌单添加一首音乐
# Check: 通过 JSON 验证 user_playlists 中某歌单的 songIds 非空
# Fallback: UI 上出现 "Added" 相关提示
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # 优先使用 JSON 验证
    playlists = c.get_user_playlists()
    if playlists and isinstance(playlists, list):
        for p in playlists:
            song_ids = p.get("songIds", [])
            if len(song_ids) > 0:
                return True

    # Fallback: UI 验证
    return (
        c.find_desc("Added")
        or c.find_text("Added to playlist")
        or c.find_text_contains("Added to")
        or c.find_text("Add to this playlist")
    )


if __name__ == "__main__":
    run_check(check, 32)
