# 引用所有检验函数
from ..base import AppTasks, TaskItem
from .test_task_01 import test1
from .test_task_02 import test2
from .test_task_03 import test3
from .test_task_04 import test4
from .test_task_05 import test5
from .test_task_06 import test6
from .test_task_07 import test7
from .test_task_08 import test8
from .test_task_09 import test9
from .test_task_10 import test10
from .test_task_11 import test11
from .test_task_12 import test12
from .test_task_13 import test13
from .test_task_14 import test14
from .test_task_15 import test15
from .test_task_16 import test16
from .test_task_17 import test17
from .test_task_18 import test18
from .test_task_19 import test19
from .test_task_20 import test20
from .test_task_21 import test21
from .test_task_22 import test22
from .test_task_23 import test23
from .test_task_24 import test24
from .test_task_25 import test25
from .test_task_26 import test26
from .test_task_27 import test27
from .test_task_28 import test28
from .test_task_29 import test29
from .test_task_30 import test30
from .test_task_31 import test31
from .test_task_32 import eval_32
from .test_task_33 import eval_33
from .test_task_34 import eval_34
from .test_task_35 import eval_35
from .test_task_36 import eval_36
from .test_task_37 import eval_37
from .test_task_38 import eval_38
from .test_task_39 import eval_39

# 所有指令
MUSIC_TASKS = AppTasks(
    package_name="com.example.mymusic",
    task_items=[
        TaskItem(
            instruction="进入我的",
            verify_func=test1,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入收藏",
            verify_func=test2,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入我的",
            verify_func=test3,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放每日推荐的歌曲",
            verify_func=test4,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="暂停播放当前的歌曲",
            verify_func=test5,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放上一首歌曲",
            verify_func=test6,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放模式改为随机播放",
            verify_func=test7,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="收藏当前歌曲",
            verify_func=test8,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="调节播放音量",
            verify_func=test9,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="随机进入'我的'一个歌单",
            verify_func=test10,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放'每日推荐'中的第一首歌曲",
            verify_func=test11,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="创建歌单,并添加1首音乐",
            verify_func=test12,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索'稻香'并播放第一首搜索结果",
            verify_func=test13,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索一个歌手，进入歌手主页，播放第一首歌",
            verify_func=test14,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="点击当前播放的歌曲，查看歌曲详情",
            verify_func=test15,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看一首歌曲的歌词",
            verify_func=test16,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='漫游播放并设置播放场景为"欢快"',
            verify_func=test17,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入排行榜的新歌榜,告诉我榜单名称",
            verify_func=test18,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="在排行榜中打开一个榜单并播放第一首歌曲",
            verify_func=test19,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="在推荐歌单中收藏一个歌单",
            verify_func=test20,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="删除第一首歌",
            verify_func=test21,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看每周、每月听歌时长",
            verify_func=test22,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="取消收藏第一首歌曲",
            verify_func=test23,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="对一首歌曲发表评论",
            verify_func=test24,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入个人听歌时长页面,告诉我本周听歌时长是多少",
            verify_func=test25,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="使用听歌识曲功能识别一首歌曲",
            verify_func=test26,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="更改歌单的排序顺序",
            verify_func=test27,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索一个歌手,选择一个专辑并收藏",
            verify_func=test28,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="删除一位关注的歌手",
            verify_func=test29,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索一位歌手，进入歌手主页播放一个MV",
            verify_func=test30,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="更改播放器样式",
            verify_func=test31,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="数一下歌曲晴天的评论的数目",
            verify_func=eval_32,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="数一下我喜欢的音乐有几首",
            verify_func=eval_33,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="计算我的歌单中每日推荐和热歌榜中一共歌曲数目",
            verify_func=eval_34,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="数一下你喜欢的歌曲推荐数目",
            verify_func=eval_35,
            human_steps=1,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="数一下我的粉丝数目",
            verify_func=eval_36,
            human_steps=1,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="数一下排行榜歌曲数目",
            verify_func=eval_37,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="数一下精选歌单歌曲数目",
            verify_func=eval_38,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="搜索歌手'周杰伦'，计算歌曲总数",
            verify_func=eval_39,
            human_steps=3,
            is_reasoning=True,
        ),
    ],
)
