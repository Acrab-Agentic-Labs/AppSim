from ..base import AppTasks, TaskItem
from .check_1 import check as check_1
from .check_2 import check as check_2
from .check_3 import check as check_3
from .check_4 import check as check_4
from .check_5 import check as check_5
from .check_6 import check as check_6
from .check_7 import check as check_7
from .check_8 import check as check_8
from .check_9 import check as check_9
from .check_10 import check as check_10
from .check_11 import check as check_11
from .check_12 import check as check_12
from .check_13 import check as check_13
from .check_14 import check as check_14
from .check_15 import check as check_15
from .check_16 import check as check_16
from .check_17 import check as check_17
from .check_18 import check as check_18
from .check_19 import check as check_19
from .check_20 import check as check_20
from .check_21 import check as check_21
from .check_22 import check as check_22
from .check_23 import check as check_23
from .check_24 import check as check_24
from .check_25 import check as check_25
from .check_26 import check as check_26
from .check_27 import check as check_27
from .check_28 import check as check_28
from .check_29 import check as check_29
from .check_30 import check as check_30
from .check_31 import check as check_31
from .check_32 import check as check_32
from .check_33 import check as check_33
from .check_34 import check as check_34
from .check_35 import check as check_35
from .check_36 import check as check_36
from .check_37 import check as check_37
from .check_38 import check as check_38
from .check_39 import check as check_39
from .check_40 import check as check_40

def validate_task(task_id):
    """Wrapper to convert check function to validate function signature"""
    def wrapper(result=None, device_id=None, backup_dir=None):
        from .check_common import AppChecker
        checker = AppChecker(device_id)
        check_func = globals()[f'check_{task_id}']
        try:
            passed = check_func(checker)
            return passed
        except Exception:
            return False
    return wrapper

SPOTIFY_TASKS = AppTasks(
    package_name="com.example.myspotify",
    task_items=[
        TaskItem(
            instruction="查看当前用户名称",
            verify_func=validate_task(1),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="当前播放歌曲的名称",
            verify_func=validate_task(2),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="数一下搜索页面共有多少种分类",
            verify_func=validate_task(3),
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看我的歌单数量",
            verify_func=validate_task(4),
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="告诉我播客页面第一条播客的标题",
            verify_func=validate_task(5),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看我关注的艺人数量",
            verify_func=validate_task(6),
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看我喜欢的歌曲数量",
            verify_func=validate_task(7),
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="播放我的第一个歌单",
            verify_func=validate_task(8),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索歌曲'Shape of You'",
            verify_func=validate_task(9),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="关注艺人'Taylor Swift'",
            verify_func=validate_task(10),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="给当前播放的歌曲点赞",
            verify_func=validate_task(11),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="创建一个新歌单，名称为'My Favorites'",
            verify_func=validate_task(12),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将当前播放的歌曲添加到'My Favorites'歌单",
            verify_func=validate_task(13),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放艺人'Ed Sheeran'的热门歌曲",
            verify_func=validate_task(14),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看'Today's Top Hits'歌单",
            verify_func=validate_task(15),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将'Shape of You'添加到'My Favorites'歌单",
            verify_func=validate_task(16),
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放播客'How AI is Changing Music'",
            verify_func=validate_task(17),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="取消关注艺人'Taylor Swift'",
            verify_func=validate_task(18),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="从'My Favorites'歌单中移除一首歌",
            verify_func=validate_task(19),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索并播放专辑'Divide'",
            verify_func=validate_task(20),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看我的播放历史",
            verify_func=validate_task(21),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="开启随机播放模式",
            verify_func=validate_task(22),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="设置播放模式为单曲循环",
            verify_func=validate_task(23),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="调整音量到50%",
            verify_func=validate_task(24),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="跳到下一首歌",
            verify_func=validate_task(25),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="返回上一首歌",
            verify_func=validate_task(26),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="暂停当前播放",
            verify_func=validate_task(27),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="继续播放",
            verify_func=validate_task(28),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看当前歌曲的歌词",
            verify_func=validate_task(29),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="分享当前播放的歌曲",
            verify_func=validate_task(30),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看推荐的歌曲",
            verify_func=validate_task(31),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="播放'Discover Weekly'歌单",
            verify_func=validate_task(32),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="搜索并关注播客'The Daily'",
            verify_func=validate_task(33),
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看我的下载内容",
            verify_func=validate_task(34),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="开启离线模式",
            verify_func=validate_task(35),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看最近播放的艺人",
            verify_func=validate_task(36),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将当前歌曲添加到队列",
            verify_func=validate_task(37),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="清空播放队列",
            verify_func=validate_task(38),
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="查看我的听歌统计",
            verify_func=validate_task(39),
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="修改歌单'My Favorites'的名称为'Best Songs'",
            verify_func=validate_task(40),
            human_steps=4,
            is_reasoning=False,
        ),
    ],
)
