from ..base import AppTasks, TaskItem
from .eval_1 import task1_friend_message_send_check
from .eval_2 import task2_group_message_send_check
from .eval_3 import task3_validate_attendee_count
from .eval_4 import TASK4_ANSWER_SCHEMA, task4_validate_friend_count
from .eval_5 import task5_validate_info_in_group
from .eval_6 import task6_validate_forward_message
from .eval_7 import task7_stared_moments_count
from .eval_8 import task8_moments_count
from .eval_9 import task9_song_name_check
from .eval_10 import task10_validate_latest_friend_like_count
from .eval_11 import TASK11_ANSWER_SCHEMA, task11_validate_financial_report_person
from .eval_12 import task12_validate_design_draft_person
from .eval_13 import task13_validate_panda_message
from .eval_14 import task14_validate_movie_message
from .eval_15 import task15_validate_restaurant_message
from .eval_16 import task16_validate_cat_dog_messages

# 所有测试指令列表（共16条，instruction 完全匹配需求描述）
WECHAT_TASKS = AppTasks(
    package_name="com.example.fakewechat",
    task_items=[
        TaskItem(
            instruction='发信息给何凯老师，说"何老师，请明天早上10点来1118会议室开会"',
            verify_func=task1_friend_message_send_check,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='发信息到工作群，说"GUI Agent最近很火，我觉得挺有意思的"',
            verify_func=task2_group_message_send_check,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看北京大学李老师发给我的信息，看看参会的听众人数是多少，我好提前去订会议室。把你的答案放置在<ans>和</ans>之间，你的答案必须是一个阿拉伯数字。",
            verify_func=task3_validate_attendee_count,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看看我有多少个微信好友。",
            verify_func=task4_validate_friend_count,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK4_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看看幸福一家人群，确定一下周六几点集合？在哪集合？把你的答案放置在<ans>和</ans>之间，你的答案必须包含集合时间和集合地点。",
            verify_func=task5_validate_info_in_group,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='看看微信好友"同事"发给我的最新消息，阅读他交代我的事情，按他说的做。',
            verify_func=task6_validate_forward_message,
            human_steps=19,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='从"发现"进入我的朋友圈，看前五条好友朋友圈，告诉我，我已经点赞了多少条。把你的答案放置在<ans>和</ans>之间，你的答案必须是一个阿拉伯数字。',
            verify_func=task7_stared_moments_count,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看看12号到15号这几天，我的好友一共发了多少条朋友圈。把你的答案放置在<ans>和</ans>之间，你的答案必须是一个阿拉伯数字。",
            verify_func=task8_moments_count,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="好友张杰的新歌名字叫什么来着，有点忘记了，你翻一下我和他的聊天记录。把你的答案放置在<ans>和</ans>之间，你的答案必须是歌曲名。",
            verify_func=task9_song_name_check,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='从"发现"进入我的朋友圈，依次浏览好友朋友圈，看看张杰最新一个朋友圈有多少人给他点赞了。把你的答案放置在<ans>和</ans>之间，你的答案必须是一个阿拉伯数字。',
            verify_func=task10_validate_latest_friend_like_count,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看工作讨论组的消息，谁完成了财务报表？",
            verify_func=task11_validate_financial_report_person,
            human_steps=7,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK11_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看工作讨论组的消息，是谁完成了设计稿？把你的答案放置在<ans>和</ans>之间，你的答案必须是人名。",
            verify_func=task12_validate_design_draft_person,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='从"发现"进入朋友圈，浏览好友朋友圈，找到第一个发大熊猫朋友圈的好友，给他发消息："大熊猫好可爱啊！是哪里的动物园呀？"',
            verify_func=task13_validate_panda_message,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='从"发现"进入朋友圈，浏览好友朋友圈，找到第一个推荐电影的好友，然后发消息问她："是什么电影呀？可以给我讲一下是什么主题的吗？"',
            verify_func=task14_validate_movie_message,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='从"发现"进入朋友圈，浏览好友朋友圈，找到第一个分享网红餐厅的好友，发消息问一下她："是哪家餐厅呀？主打菜是什么？"',
            verify_func=task15_validate_restaurant_message,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='从"发现"进入朋友圈，浏览好友朋友圈，给第一个分享小猫朋友圈的好友和第一个分享小狗朋友圈的好友分别发送"你的猫好可爱！"和"你的狗好可爱！"',
            verify_func=task16_validate_cat_dog_messages,
            human_steps=14,
            is_reasoning=False,
        ),
    ],
)
