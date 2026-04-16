# Task 14: 将当前播放歌曲收藏
# Check: 通过 JSON 验证 likedSongs 数量是否比初始值增加
# Fallback: UI 上出现 "Unlike" 图标
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        liked = state.get("likedSongs", [])
        # 初始有 2 首 liked songs，收藏后应该 > 2 或包含当前歌曲
        if len(liked) > len(c.INITIAL_LIKED_SONGS):
            return True
        # 检查 song_013 (IRIS OUT, 默认播放歌曲) 是否被收藏
        if "song_013" in liked:
            return True

    # Fallback: UI 验证
    return c.find_desc("Unlike")


if __name__ == "__main__":
    run_check(check, 14)
