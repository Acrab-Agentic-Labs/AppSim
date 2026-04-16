# Task 29: 关注一个新的播客
# Check: 通过 JSON 验证 savedPodcasts 数量是否增加（初始为空）
# Fallback: UI 上出现 "Following" 按钮
from check_common import AppChecker, run_check


def check(c: AppChecker):
    # 优先使用 JSON 验证
    state = c.get_user_state()
    if state:
        podcasts = state.get("savedPodcasts", [])
        # 初始没有关注播客，关注后应 > 0
        if len(podcasts) > 0:
            return True

    # Fallback: UI 验证
    return (
        c.find_text("Following")
        and (
            c.find_text("Add podcasts")
            or c.find_text_contains("Podcasts you might like")
        )
    )


if __name__ == "__main__":
    run_check(check, 29)
