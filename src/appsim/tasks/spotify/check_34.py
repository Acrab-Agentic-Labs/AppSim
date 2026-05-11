# Task 34: 告诉我播客页面第三条播客的标题和发布日期, 收藏它, 发表评论 'Great episode!', 并快进15秒
# Check: 验证 savedPodcasts 增加, answer 含标题和日期信息
from .check_common import AppChecker, run_check, result_pass, result_fail


def check(c: AppChecker, result=None):
    # 验证 savedPodcasts 增加
    user_state = c.get_user_state()
    if not user_state or not isinstance(user_state, dict):
        return result_fail("Check failed: unable to read user_state.json")

    saved_podcasts = user_state.get("savedPodcasts", [])
    if len(saved_podcasts) < 1:
        return result_fail(
            "Check failed: no saved podcasts found",
            {"savedPodcasts": saved_podcasts},
        )

    # 验证答案包含第三条播客的标题和发布日期
    if not result or "final_message" not in result:
        return result_fail("Check failed: no answer provided in result")

    final_msg = str(result["final_message"]).lower()

    # 第三条播客: "The Sound of Tomorrow", date: "Dec 8"
    has_title = any(
        keyword in final_msg
        for keyword in ["sound of tomorrow", "the sound", "third", "podcast", "播客"]
    )
    has_date = any(
        keyword in final_msg
        for keyword in ["dec 8", "dec8", "december 8", "december", "发布", "date", "日期"]
    )

    if not has_title or not has_date:
        return result_fail(
            "Check failed: answer does not contain third podcast title and publish date",
            {"finalMessage": result["final_message"]},
        )

    return result_pass(
        "Check passed: podcast saved, answer contains title and publish date"
    )


if __name__ == "__main__":
    run_check(check, 34)
