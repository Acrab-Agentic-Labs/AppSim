# 引用所有检验函数
from ..base import AppTasks, TaskItem
from .eval_1 import message_send_check
from .eval_2 import browse_notes_check
from .eval_3 import search_and_view_check
from .eval_4 import like_collect_comment_check
from .eval_5 import follow_author_check
from .eval_6 import reply_comment_check
from .eval_7 import browsing_history_check
from .eval_8 import dislike_note_check
from .eval_9 import browsing_history_check
from .eval_10 import set_password_check
from .eval_11 import change_nickname_check
from .eval_12 import publish_note_check
from .eval_13 import share_note_check
from .eval_14 import send_message_check
from .eval_15 import like_comment_check
from .eval_16 import browse_and_interact_check
from .eval_17 import search_result_count_check
from .eval_18 import publish_and_self_interact_check
from .eval_19 import note_interaction_check
from .eval_20 import follow_back_fan_check
from .eval_21 import view_and_comment_notes_check
from .eval_22 import count_author_notes_check, TASK22_ANSWER_SCHEMA
from .eval_23 import unfollow_author_check
from .eval_24 import TASK24_ANSWER_SCHEMA, eval_24
from .eval_25 import TASK25_ANSWER_SCHEMA, eval_25
from .eval_26 import TASK26_ANSWER_SCHEMA, eval_26
from .eval_27 import find_tie_method
from .eval_28 import eval_28, TASK28_ANSWER_SCHEMA
from .eval_29 import eval_29, TASK29_ANSWER_SCHEMA

# 所有指令
RED_NOTE_TASKS = AppTasks(
    package_name="com.example.rednote_sim",
    task_items=[
        TaskItem(
            instruction='给博主"小红薯美妆达人"发消息"你好"',
            verify_func=message_send_check,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="总结首页前3篇笔记内容",
            verify_func=browse_notes_check,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='搜索"秋冬穿搭"，总结搜索结果前3条内容详情',
            verify_func=search_and_view_check,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索并打开一篇标题含'穿搭'的笔记，对其进行点赞、收藏并评论'很有用！'",
            verify_func=like_collect_comment_check,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="关注博主'小红薯美妆达人'。",
            verify_func=follow_author_check,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看评论和@你的消息，回复最新收到的一条评论，内容为'谢谢喜欢～'",
            verify_func=reply_comment_check,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="总结你关注的第一个博主的第一条笔记",
            verify_func=browsing_history_check,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="对首页第二篇笔记选择'不喜欢'。",
            verify_func=dislike_note_check,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="总结你收藏的第一篇笔记的内容",
            verify_func=browsing_history_check,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将'我'的登录密码设置为123456",
            verify_func=set_password_check,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将自己的名字修改为'111'",
            verify_func=change_nickname_check,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="发布笔记，内容为'天晴了'，标题为'今日份分享'，笔记设为'仅自己可见'",
            verify_func=publish_note_check,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将首页的第一篇笔记分别分享至朋友圈",
            verify_func=share_note_check,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="给'我'关注的第一个博主发私信'催更'",
            verify_func=send_message_check,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看首页第二篇笔记的第一条评论，对评论进行点赞",
            verify_func=like_comment_check,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="浏览前2篇首页推荐笔记，对笔记进行点赞、收藏、发送评论'很精彩'",
            verify_func=browse_and_interact_check,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'美妆'，统计搜索结果的笔记数目",
            verify_func=search_result_count_check,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="发布笔记，内容为'今天也要加油呀'，标题为'今日分享'，笔记设为'公开可见'，并对这篇笔记进行点赞、收藏",
            verify_func=publish_and_self_interact_check,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="总结你收藏的第2个笔记的内容并点赞，评论'很实用！'",
            verify_func=note_interaction_check,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="对'我'的第一个粉丝进行'回关'",
            verify_func=follow_back_fan_check,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="浏览我'赞过'的前3条笔记，并评论'很有用'",
            verify_func=view_and_comment_notes_check,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="统计博主'旅行日记'发布笔记数量",
            verify_func=count_author_notes_check,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK22_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="对'潮流时尚达人'取消关注",
            verify_func=unfollow_author_check,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="数一下我的私信的数目",
            verify_func=eval_24,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK24_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="计算我的关注和粉丝总人数",
            verify_func=eval_25,
            human_steps=1,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK25_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="数一下'潮流时尚达人'共发布的笔记数量",
            verify_func=eval_26,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK26_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="我想学习围巾的新系法，帮我推荐一篇笔记并打开",
            verify_func=find_tie_method,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查找我的小红书号",
            verify_func=eval_28,
            human_steps=1,
            is_reasoning=False,
            evaluation_type="answer",
            answer_schema=TASK28_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="告诉我我关注的博主中最受大众关注的是谁",
            verify_func=eval_29,
            human_steps=21,
            is_reasoning=False,
            evaluation_type="answer",
            answer_schema=TASK29_ANSWER_SCHEMA,
        ),
    ],
)
