# Task 40: 告诉我有声书第一条内容的标题和发布日期, 播放并收藏它, 发表评论 'Great episode!',
# 并快进15秒，然后收藏第二本有声书
# Check: 验证 savedAudiobooks >= 2, answer 含标题和日期信息
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 验证 savedAudiobooks 至少有2本
    user_state = c.get_user_state()
    if not user_state or not isinstance(user_state, dict):
        return result_fail("Check failed: unable to read user_state.json")

    saved_audiobooks = user_state.get("savedAudiobooks", [])
    if len(saved_audiobooks) < 2:
        return result_fail(
            f"Check failed: saved audiobooks count is {len(saved_audiobooks)}, expected at least 2",
            {"savedAudiobooks": saved_audiobooks},
        )

    # 验证答案包含第一本有声书的标题和发布日期
    if not result or "final_message" not in result:
        return result_fail("Check failed: no answer provided in result")

    final_msg = str(result["final_message"]).lower()

    # 第一本有声书: "The Art of Reading" by James Clear
    has_title = any(
        keyword in final_msg
        for keyword in ["art of reading", "the art", "audiobook", "有声书"]
    )
    has_date = any(
        keyword in final_msg
        for keyword in ["date", "publish", "发布", "日期", "20"]
    )

    if not has_title or not has_date:
        return result_fail(
            "Check failed: answer does not contain first audiobook title and publish date",
            {"finalMessage": result["final_message"]},
        )

    return result_pass(
        f"Check passed: {len(saved_audiobooks)} audiobooks saved, answer contains title and date"
    )


if __name__ == "__main__":
    run_check(check, 40)
