# Task 37: 随机收藏一本有声书
# Check: 通过 JSON 验证 savedAudiobooks 数量是否增加（初始为空）
# Fallback: UI 上出现有声书详情页且 "Saved" 状态
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        audiobooks = state.get("savedAudiobooks", [])
        # 初始没有收藏有声书，收藏后应 > 0
        if len(audiobooks) > 0:
            return True

    # Fallback: UI 验证
    return (
        c.find_desc("Back")
        and c.find_text("About this book")
        and c.find_desc("Saved")
    )


if __name__ == "__main__":
    run_check(check, 37)
