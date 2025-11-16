# 引用所有检验函数
from ..base import TaskItem, AppTasks

# 导入验证函数（对应所有测试场景）
from .eval_1 import CheckWatchHistory
from .eval_2 import validate_task_2
from .eval_3 import CheckSearchGame
from .eval_4 import validate_task_4
from .eval_5 import CheckLikeVideo
from .eval_6 import validate_task_6
from .eval_7 import CheckFavoriteVideo
from .eval_8 import CheckWatchRecommend
from .eval_9 import CheckProfilePage
from .eval_10 import CheckFullscreen
from .eval_11 import validate_task_11
from .eval_12 import CheckOfflineCache
from .eval_13 import validate_task_13
from .eval_14 import validate_task_14
from .eval_15 import validate_task_15
from .eval_16 import CheckReplyComment
from .eval_17 import validate_task_17
from .eval_18 import validate_task_18
from .eval_19 import validate_task_19
from .eval_20 import CheckSearchGame1
from .eval_21 import validate_task_21
from .eval_22 import CheckSearchPlayLike
from .eval_23 import validate_task_23
from .eval_24 import validate_task_24
from .eval_25 import validate_task_25
from .eval_26 import CheckHistoryItemDelete
from .eval_27 import validate_task_27
from .eval_28 import validate_task_28
from .eval_29 import validate_task_29
from .eval_30 import validate_task_30

# 所有测试指令列表
BILIBILI_TASKS = AppTasks(
    package_name="com.example.bilibili",
    task_items=[
        TaskItem(instruction="查看我的观看历史。", verify_func=CheckWatchHistory),
        TaskItem(instruction="看一下私信智能拦截的开启状态。", verify_func=validate_task_2),
        TaskItem(instruction="搜索游戏解说。", verify_func=CheckSearchGame),
        TaskItem(instruction="看一下首页罗翔老师的视频点赞加投币一共多少。", verify_func=validate_task_4),
        TaskItem(instruction="看第一个视频，点赞。", verify_func=CheckLikeVideo),
        TaskItem(instruction="看看会员购里的商品全部买下来要多少钱。", verify_func=validate_task_6),
        TaskItem(instruction="看第一个视频，点击收藏。", verify_func=CheckFavoriteVideo),
        TaskItem(instruction="在首页观看一条推荐中的视频。", verify_func=CheckWatchRecommend),
        TaskItem(instruction="进入我的个人资料页查看我追的动漫叫什么。", verify_func=CheckProfilePage),
        TaskItem(instruction="看第一个视频，进入全屏模式观看。", verify_func=CheckFullscreen),
        TaskItem(instruction="在关注列表去UP主逍遥散人主页查看其粉丝数。", verify_func=validate_task_11),
        TaskItem(instruction="进入离线缓存页面。", verify_func=CheckOfflineCache),
        TaskItem(instruction="进入第一个视频，看第四个相关视频的up主名字叫什么。", verify_func=validate_task_13),
        TaskItem(instruction="查看关注动态中所有动态的点赞数加播放量一共多少。", verify_func=validate_task_14),
        TaskItem(instruction="数一下关注列表有几个已互粉的up主。", verify_func=validate_task_15),
        TaskItem(instruction='对首页第一条视频评论，点击回复，输入"谢谢分享！"并发送。', verify_func=CheckReplyComment),
        TaskItem(
            instruction="看第一个视频，不算我点的赞，看看评论区所有赞加起来有多少。", verify_func=validate_task_17
        ),
        TaskItem(instruction="看一下接收消息通知总开关的状态。", verify_func=validate_task_18),
        TaskItem(
            instruction="在首页推荐第一个视频评论页面，查看等级最低的那个人的被回复评论的点赞数。",
            verify_func=validate_task_19,
        ),
        TaskItem(instruction="搜索游戏解说，查看本次搜索共找到多少个结果。", verify_func=CheckSearchGame1),
        TaskItem(instruction="看第一个视频，查看相关视频有几个。", verify_func=validate_task_21),
        TaskItem(instruction='搜索视频"游戏解说"，播放搜索出的第一个视频并点赞。', verify_func=CheckSearchPlayLike),
        TaskItem(instruction="查看收藏的第一个视频的视频时长。", verify_func=validate_task_23),
        TaskItem(instruction="在收藏页面查看该收藏中共收藏了多少个视频。", verify_func=validate_task_24),
        TaskItem(instruction="去设置里找一下uid是多少。", verify_func=validate_task_25),
        TaskItem(
            instruction="在历史记录页面，找到今天观看过的一个视频，长按该记录项，将其从历史记录中删除，然后告诉我删除后还有几个视频。",
            verify_func=CheckHistoryItemDelete,
        ),
        TaskItem(
            instruction="在首页第一条视频评论页面，找到一条点赞数最高的评论，看看up主的名字叫什么。",
            verify_func=validate_task_27,
        ),
        TaskItem(instruction="在设置中，查看当前定时关闭状态。", verify_func=validate_task_28),
        TaskItem(
            instruction="在直播推荐页面，查看直播人数最少的两个的在线观看人数一共多少。", verify_func=validate_task_29
        ),
        TaskItem(instruction="看一下会员购里的商品一共卖了多少件。。", verify_func=validate_task_30),
    ],
)

# 为了向后兼容，保留 ALL_INSTRUCTION
ALL_INSTRUCTION = [{"instruct": item.instruction, "fun": item.verify_func} for item in BILIBILI_TASKS.task_items]
