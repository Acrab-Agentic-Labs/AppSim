from ..base import AppTasks, NumericReasoningCategory, TaskItem
from .eval_1 import verify_private_message_sent
from .eval_2 import verify_group_message_sent
from .eval_3 import TASK3_ANSWER_SCHEMA, verify_meeting_attendee_count
from .eval_4 import TASK4_ANSWER_SCHEMA, verify_friend_count
from .eval_5 import TASK5_ANSWER_SCHEMA, verify_group_event_details
from .eval_6 import verify_latest_message_instructions_completed
from .eval_7 import TASK7_ANSWER_SCHEMA, verify_liked_moments_count
from .eval_8 import TASK8_ANSWER_SCHEMA, verify_moments_count
from .eval_9 import TASK9_ANSWER_SCHEMA, verify_song_name_retrieved
from .eval_10 import TASK10_ANSWER_SCHEMA, verify_friend_moments_like_count
from .eval_11 import TASK11_ANSWER_SCHEMA, verify_financial_report_assignee_identified
from .eval_12 import TASK12_ANSWER_SCHEMA, verify_design_draft_assignee_identified
from .eval_13 import verify_moment_author_message_sent
from .eval_14 import verify_moment_author_question_sent
from .eval_15 import verify_moment_author_information_requested
from .eval_16 import verify_multiple_moment_authors_contacted

# 所有测试指令列表（共16条，instruction 完全匹配需求描述）
WECHAT_TASKS = AppTasks(
    package_name="com.example.fakewechat",
    task_items=[
        TaskItem(
            instruction='发信息给何凯老师，说"何老师，请明天早上10点来1118会议室开会"',
            verify_func=verify_private_message_sent,
            human_steps=8,
        ),
        TaskItem(
            instruction='发信息到工作群，说"GUI Agent最近很火，我觉得挺有意思的"',
            verify_func=verify_group_message_sent,
            human_steps=7,
        ),
        TaskItem(
            instruction="查看北京大学李老师发给我的信息，看看参会的听众人数是多少，我好提前去订会议室。",
            verify_func=verify_meeting_attendee_count,
            human_steps=5,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK3_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看看我有多少个微信好友。",
            verify_func=verify_friend_count,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK4_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看看幸福一家人群，确定一下周六几点集合？在哪集合？",
            verify_func=verify_group_event_details,
            human_steps=5,
            evaluation_type="answer",
            answer_schema=TASK5_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='看看微信好友"同事"发给我的最新消息，阅读他交代我的事情，按他说的做。',
            verify_func=verify_latest_message_instructions_completed,
            human_steps=19,
        ),
        TaskItem(
            instruction='从"发现"进入我的朋友圈，看前五条好友朋友圈，告诉我，我已经点赞了多少条。',
            verify_func=verify_liked_moments_count,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK7_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看看12号到15号这几天，我的好友一共发了多少条朋友圈。",
            verify_func=verify_moments_count,
            human_steps=5,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK8_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="好友张杰的新歌名字叫什么来着，有点忘记了，你翻一下我和他的聊天记录。",
            verify_func=verify_song_name_retrieved,
            human_steps=6,
            evaluation_type="answer",
            answer_schema=TASK9_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='从"发现"进入我的朋友圈，依次浏览好友朋友圈，看看张杰最新一个朋友圈有多少人给他点赞了。',
            verify_func=verify_friend_moments_like_count,
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK10_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看工作讨论组的消息，谁完成了财务报表？",
            verify_func=verify_financial_report_assignee_identified,
            human_steps=7,
            evaluation_type="answer",
            answer_schema=TASK11_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看工作讨论组的消息，是谁完成了设计稿？",
            verify_func=verify_design_draft_assignee_identified,
            human_steps=7,
            evaluation_type="answer",
            answer_schema=TASK12_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='从"发现"进入朋友圈，浏览好友朋友圈，找到第一个发大熊猫朋友圈的好友，给他发消息："大熊猫好可爱啊！是哪里的动物园呀？"',
            verify_func=verify_moment_author_message_sent,
            human_steps=12,
        ),
        TaskItem(
            instruction='从"发现"进入朋友圈，浏览好友朋友圈，找到第一个推荐电影的好友，然后发消息问她："是什么电影呀？可以给我讲一下是什么主题的吗？"',
            verify_func=verify_moment_author_question_sent,
            human_steps=12,
        ),
        TaskItem(
            instruction='从"发现"进入朋友圈，浏览好友朋友圈，找到第一个分享网红餐厅的好友，发消息问一下她："是哪家餐厅呀？主打菜是什么？"',
            verify_func=verify_moment_author_information_requested,
            human_steps=15,
        ),
        TaskItem(
            instruction='从"发现"进入朋友圈，浏览好友朋友圈，给第一个分享小猫朋友圈的好友和第一个分享小狗朋友圈的好友分别发送"你的猫好可爱！"和"你的狗好可爱！"',
            verify_func=verify_multiple_moment_authors_contacted,
            human_steps=14,
        ),
    ],
)
