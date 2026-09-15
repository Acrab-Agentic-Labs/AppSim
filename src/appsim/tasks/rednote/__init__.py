# 引用所有检验函数
from ..base import AppTasks, TaskItem
from .eval_1 import verify_author_message_sent
from .eval_2 import verify_homepage_notes_summarized
from .eval_3 import verify_searched_notes_summarized
from .eval_4 import verify_note_liked_collected_and_commented
from .eval_5 import verify_author_followed
from .eval_6 import verify_latest_comment_replied
from .eval_7 import verify_followed_author_note_summarized
from .eval_8 import verify_homepage_note_disliked
from .eval_9 import verify_collected_note_summarized
from .eval_10 import verify_account_password_updated
from .eval_11 import verify_profile_name_updated
from .eval_12 import verify_private_note_published
from .eval_13 import verify_note_shared
from .eval_14 import verify_followed_author_message_sent
from .eval_15 import verify_note_comment_liked
from .eval_16 import verify_homepage_notes_interacted_with
from .eval_17 import verify_search_result_note_count
from .eval_18 import verify_public_note_published_and_interacted_with
from .eval_19 import verify_collected_note_liked_and_commented
from .eval_20 import verify_fan_followed_back
from .eval_21 import verify_liked_notes_commented
from .eval_22 import verify_author_note_count_from_profile, TASK22_ANSWER_SCHEMA
from .eval_23 import verify_author_unfollowed
from .eval_24 import TASK24_ANSWER_SCHEMA, verify_private_message_count
from .eval_25 import TASK25_ANSWER_SCHEMA, verify_following_and_follower_count
from .eval_26 import TASK26_ANSWER_SCHEMA, verify_author_note_count_from_notes
from .eval_27 import verify_recommended_note_opened
from .eval_28 import verify_account_identifier_retrieved, TASK28_ANSWER_SCHEMA
from .eval_29 import verify_most_followed_author_identified, TASK29_ANSWER_SCHEMA

# 所有指令
RED_NOTE_TASKS = AppTasks(
    package_name="com.example.rednote_sim",
    task_items=[
        TaskItem(
            instruction='给博主"小红薯美妆达人"发消息"你好"',
            verify_func=verify_author_message_sent,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="总结首页前3篇笔记内容",
            verify_func=verify_homepage_notes_summarized,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='搜索"秋冬穿搭"，总结搜索结果前3条内容详情',
            verify_func=verify_searched_notes_summarized,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索并打开一篇标题含'穿搭'的笔记，对其进行点赞、收藏并评论'很有用！'",
            verify_func=verify_note_liked_collected_and_commented,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="关注博主'小红薯美妆达人'。",
            verify_func=verify_author_followed,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看评论和@你的消息，回复最新收到的一条评论，内容为'谢谢喜欢～'",
            verify_func=verify_latest_comment_replied,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="总结你关注的第一个博主的第一条笔记",
            verify_func=verify_followed_author_note_summarized,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="对首页第二篇笔记选择'不喜欢'。",
            verify_func=verify_homepage_note_disliked,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="总结你收藏的第一篇笔记的内容",
            verify_func=verify_collected_note_summarized,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将'我'的登录密码设置为123456",
            verify_func=verify_account_password_updated,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将自己的名字修改为'111'",
            verify_func=verify_profile_name_updated,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="发布笔记，内容为'天晴了'，标题为'今日份分享'，笔记设为'仅自己可见'",
            verify_func=verify_private_note_published,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将首页的第一篇笔记分别分享至朋友圈",
            verify_func=verify_note_shared,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="给'我'关注的第一个博主发私信'催更'",
            verify_func=verify_followed_author_message_sent,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看首页第二篇笔记的第一条评论，对评论进行点赞",
            verify_func=verify_note_comment_liked,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="浏览前2篇首页推荐笔记，对笔记进行点赞、收藏、发送评论'很精彩'",
            verify_func=verify_homepage_notes_interacted_with,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'美妆'，统计搜索结果的笔记数目",
            verify_func=verify_search_result_note_count,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="发布笔记，内容为'今天也要加油呀'，标题为'今日分享'，笔记设为'公开可见'，并对这篇笔记进行点赞、收藏",
            verify_func=verify_public_note_published_and_interacted_with,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="总结你收藏的第2个笔记的内容并点赞，评论'很实用！'",
            verify_func=verify_collected_note_liked_and_commented,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="对'我'的第一个粉丝进行'回关'",
            verify_func=verify_fan_followed_back,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="浏览我'赞过'的前3条笔记，并评论'很有用'",
            verify_func=verify_liked_notes_commented,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="统计博主'旅行日记'发布笔记数量",
            verify_func=verify_author_note_count_from_profile,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK22_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="对'潮流时尚达人'取消关注",
            verify_func=verify_author_unfollowed,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="数一下我有多少条私信消息",
            verify_func=verify_private_message_count,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK24_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="计算我的关注和粉丝总人数",
            verify_func=verify_following_and_follower_count,
            human_steps=1,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK25_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="数一下'潮流时尚达人'共发布的笔记数量",
            verify_func=verify_author_note_count_from_notes,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK26_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="我想学习围巾的新系法，帮我推荐一篇笔记并打开",
            verify_func=verify_recommended_note_opened,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查找我的小红书号",
            verify_func=verify_account_identifier_retrieved,
            human_steps=1,
            is_reasoning=False,
            evaluation_type="answer",
            answer_schema=TASK28_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="告诉我我关注的博主中最受大众关注的是谁",
            verify_func=verify_most_followed_author_identified,
            human_steps=21,
            is_reasoning=False,
            evaluation_type="answer",
            answer_schema=TASK29_ANSWER_SCHEMA,
        ),
    ],
)
