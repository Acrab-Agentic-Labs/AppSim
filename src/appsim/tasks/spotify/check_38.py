# Task 38: 创建一个新的歌单并添加两首新的歌曲
# Check: 通过 JSON 验证存在新歌单且包含至少2首歌，并且UI在歌单详情页
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker):
    # 必须在歌单详情页，而不是添加歌曲的选择页面
    ui_passed = (
        c.find_desc("Back")
        and (
            c.find_desc("Shuffle")
            or c.find_text_contains("songs")
            or c.find_desc("Play")
        )
        and not c.find_text("Add to playlist")  # 不在添加歌曲页面
    )

    if not ui_passed:
        return result_fail("UI check failed: not on playlist detail page")

    # 验证 JSON 中存在新歌单且包含至少2首歌
    playlists = c.get_user_playlists()
    if not playlists or not isinstance(playlists, list):
        return result_fail("Check failed: unable to read user_playlists.json")

    for p in playlists:
        song_ids = p.get("songIds", [])
        if len(song_ids) >= 2:
            return result_pass(f"Check passed: playlist '{p.get('name')}' has {len(song_ids)} songs")

    return result_fail(
        "Check failed: no user playlist with 2+ songs found",
        {"userPlaylists": playlists},
    )


if __name__ == "__main__":
    run_check(check, 38)
