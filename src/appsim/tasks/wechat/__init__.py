from ..base import AppTasks, TaskItem
from .eval_1 import Task1_MessageSendCheck
from .eval_2 import Task2_MessageSendCheck
from .eval_3 import Task3_number_count
from .eval_4 import Task4_number_count
from .eval_5 import Task5_info_search
from .eval_6 import Task6_MessageSendCheck
from .eval_7 import Task7_number_count
from .eval_8 import Task8_number_count
from .eval_9 import Task9_song_find
from .eval_10 import Task10_number_count

# 所有测试指令列表（共10条，instruct 完全匹配需求描述）
WECHAT_TASKS = AppTasks(
    package_name="com.example.fakewechat",
    task_items=[
        TaskItem(
            instruction='发信息给何凯老师，说"何老师，请明天早上10点来1118会议室开会"',
            verify_func=Task1_MessageSendCheck,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='发信息到工作群，说"GUI Agent最近很火，我觉得挺有意思的"',
            verify_func=Task2_MessageSendCheck,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看北京大学李老师发给我的信息，看看参会的听众人数是多少，我好提前去订会议室。告诉我数字即可。",
            verify_func=Task3_number_count,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看看我有多少个微信好友。告诉我数字即可。",
            verify_func=Task4_number_count,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看看幸福一家人群，确定一下周六几点集合？在哪集合？告诉我答案即可。",
            verify_func=Task5_info_search,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='看看微信好友"同事"发给我的最新消息，阅读他交代我的事情，按他说的做。',
            verify_func=Task6_MessageSendCheck,
            human_steps=19,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='从"发现"进入我的朋友圈，看前五条好友朋友圈，告诉我，我已经点赞了多少条。告诉我数字即可。',
            verify_func=Task7_number_count,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看看12号到15号这几天，我的好友一共发了多少条朋友圈。告诉我数字即可。",
            verify_func=Task8_number_count,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="好友张杰的新歌名字叫什么来着，有点忘记了，你翻一下我和他的聊天记录。告诉我答案即可。",
            verify_func=Task9_song_find,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='从"发现"进入我的朋友圈，依次浏览好友朋友圈，看看张杰最新一个朋友圈有多少人给他点赞了。告诉我数字即可。',
            verify_func=Task10_number_count,
            human_steps=3,
            is_reasoning=True,
        ),
    ],
)
