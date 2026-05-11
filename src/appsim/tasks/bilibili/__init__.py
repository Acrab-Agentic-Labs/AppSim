# 引用所有检验函数
from ..base  import TaskItem, AppTasks

# 导入验证函数（对应所有测试场景）
from .eval_1 import validate_task_1
from .eval_2 import validate_task_2
from .eval_3 import validate_task_3
from .eval_4 import CheckProfilePage
from .eval_5 import validate_task_5
from .eval_6 import validate_task_6
from .eval_7 import validate_task_7
from .eval_8 import validate_task_8
from .eval_9 import CheckReplyComment
from .eval_10 import validate_task_10
from .eval_11 import validate_task_11
from .eval_12 import validate_task_12
from .eval_13 import validate_task_13
from .eval_14 import validate_task_14
from .eval_15 import CheckHistoryItemDelete
from .eval_16 import validate_task_16
from .eval_17 import validate_task_17
from .eval_18 import validate_task_18
from .eval_19 import validate_task_19
from .eval_20 import validate_task_20
from .eval_21 import CheckVideoLikeFavoriteFullscreen
from .eval_22 import CheckSearchCountAndRelated
from .eval_23 import CheckSearchPlayLikeReply
from .eval_24 import CheckUidAndCloseChatPush
from .eval_25 import CheckFavoriteLikeComment
from .eval_26 import validate_task_26
from .eval_27 import validate_task_27
from .eval_28 import validate_task_28
from .eval_29 import CheckCacheVideoCommentAndMessageSetting

# 所有测试指令列表
BILIBILI_TASKS = AppTasks(
    package_name="com.example.bilibili_sim",
    task_items=[
        TaskItem(instruction='看一下私信智能拦截的开启状态，只回答"已开启"或者"未开启"。', verify_func=validate_task_1, human_steps=4, is_reasoning=True),
        TaskItem(instruction='看一下首页罗翔老师的第一个视频点赞加投币一共多少。', verify_func=validate_task_2, human_steps=1, is_reasoning=True),
        TaskItem(instruction='看看会员购里的前四个商品全部买下来要多少钱。', verify_func=validate_task_3, human_steps=1, is_reasoning=True),
        TaskItem(instruction='进入我的个人资料页查看我追的第一个动漫叫什么。', verify_func=CheckProfilePage, human_steps=2, is_reasoning=True),
        TaskItem(instruction='在关注列表去UP主逍遥散人主页查看其粉丝数。', verify_func=validate_task_5, human_steps=3, is_reasoning=True),
        TaskItem(instruction='进入首页第一个视频，算一下收藏加转发数量一共多少，不算上我的收藏。', verify_func=validate_task_6, human_steps=2, is_reasoning=True),
        TaskItem(instruction='查看关注动态中前十个动态的点赞数加播放量一共多少。', verify_func=validate_task_7, human_steps=2, is_reasoning=True),
        TaskItem(instruction='数一下关注列表有几个已互粉的up主。', verify_func=validate_task_8, human_steps=2, is_reasoning=True),
        TaskItem(instruction='对首页第一条视频评论，点击回复，输入"谢谢分享！"并发送。', verify_func=CheckReplyComment, human_steps=5, is_reasoning=False),
        TaskItem(instruction='看第一个视频，不算我点的赞，看看评论区前3条评论所有赞加起来有多少。', verify_func=validate_task_10, human_steps=3, is_reasoning=True),
        TaskItem(instruction='看一下接收消息通知总开关的状态。', verify_func=validate_task_11, human_steps=4, is_reasoning=True),
        TaskItem(instruction='在首页推荐第一个视频评论页面，查看前5条评论等级最低的那个人的被回复评论的点赞数', verify_func=validate_task_12, human_steps=3, is_reasoning=True),
        TaskItem(instruction='查看收藏的第一个视频的视频时长。', verify_func=validate_task_13, human_steps=2, is_reasoning=True),
        TaskItem(instruction='在收藏页面查看该收藏中共收藏了多少个视频。', verify_func=validate_task_14, human_steps=4, is_reasoning=True),
        TaskItem(instruction='在历史记录页面，找到今天观看过的一个视频，长按该记录项，将其从历史记录中删除，然后告诉我删除后还有几个视频。', verify_func=CheckHistoryItemDelete, human_steps=5, is_reasoning=True),
        TaskItem(instruction='在首页第一条视频评论页面，找到一条点赞数最高的评论，看看用户的名字叫什么。', verify_func=validate_task_16, human_steps=3, is_reasoning=True),
        TaskItem(instruction='在设置中，查看当前定时关闭状态。', verify_func=validate_task_17, human_steps=4, is_reasoning=True),
        TaskItem(instruction='在直播推荐页面，查看前四个推荐直播中人数最少的两个的在线观看人数一共多少。', verify_func=validate_task_18, human_steps=2, is_reasoning=True),
        TaskItem(instruction='看一下会员购里的前四个商品一共多少人购买。', verify_func=validate_task_19, human_steps=1, is_reasoning=True),
        TaskItem(instruction='查看大会员是否到期，回答"已到期"或者"未到期"。', verify_func=validate_task_20, human_steps=3, is_reasoning=True),
        TaskItem(instruction='看主页第一个视频，点赞，取消收藏，进入全屏模式观看。', verify_func=CheckVideoLikeFavoriteFullscreen, human_steps=7, is_reasoning=False),
        TaskItem(instruction='搜索"游戏解说"，播放第一个视频查看相关视频有几个，告诉我答案即可。', verify_func=CheckSearchCountAndRelated, human_steps=6, is_reasoning=True),
        TaskItem(instruction='搜索视频"游戏解说"，播放搜索出的第一个视频并点赞，然后对该视频评论"谢谢分享！"。', verify_func=CheckSearchPlayLikeReply, human_steps=11, is_reasoning=False),
        TaskItem(instruction='查看我的Uid并关闭推送设置中的聊天消息。', verify_func=CheckUidAndCloseChatPush, human_steps=8, is_reasoning=True),
        TaskItem(instruction='给我的收藏里第二个视频点赞并评论："谢谢up主的分享！"', verify_func=CheckFavoriteLikeComment, human_steps=7, is_reasoning=False),
        TaskItem(instruction='观看收藏夹第二个视频，查看其前20条展示的评论，评论点赞数最低的那个人是用户几号？', verify_func=validate_task_26, human_steps=11, is_reasoning=True),
        TaskItem(instruction='分别打开历史记录里的第二个视频和收藏夹里的第二个视频，查看各自评论区展示的第一条一级评论的点赞数；如果两者不同，就对点赞数更高的那个视频发送评论"这赞也太多了吧！"，如果两者相同，就对历史记录里的那个视频发送评论"这赞也太多了吧！"。', verify_func=validate_task_27, human_steps=12, is_reasoning=True),
        TaskItem(instruction='算一下我的关注列表里的前五个关注一共发了多少条视频，然后去导航栏的关注动态页面，在列表页面给逍遥散人的第一条动态点赞！', verify_func=validate_task_28, human_steps=11, is_reasoning=True),
        TaskItem(instruction='看一下离线缓存中是什么视频然后去我的收藏里观看这个视频，并给这个视频评论"张三就是有学问！"然后关闭消息设置里的消息提醒。', verify_func=CheckCacheVideoCommentAndMessageSetting, human_steps=14, is_reasoning=False),
    ]
)

# 为了向后兼容，保留 ALL_INSTRUCTION
ALL_INSTRUCTION = [
    {"instruct": item.instruction, "fun": item.verify_func}
    for item in BILIBILI_TASKS.task_items
]
