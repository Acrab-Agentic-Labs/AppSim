from ..base import AppTasks, TaskItem
from .eval_1 import validate_task_one
from .eval_2 import validate_task_two
from .eval_3 import validate_task_three
from .eval_4 import validate_task_four
from .eval_5 import validate_task_five
from .eval_6 import validate_task_six
from .eval_7 import validate_task_seven
from .eval_8 import validate_task_eight
from .eval_9 import validate_task_nine
from .eval_10 import validate_task_ten
from .eval_11 import validate_task_eleven
from .eval_12 import validate_task_twelve
from .eval_13 import validate_task_thirteen
from .eval_14 import validate_task_fourteen
from .eval_15 import validate_task_fifteen
from .eval_16 import validate_task_sixteen
from .eval_17 import validate_task_seventeen
from .eval_18 import validate_task_eighteen
from .eval_19 import validate_task_nineteen
from .eval_20 import validate_task_twenty

JD_TASKS = AppTasks(
    package_name="com.example.MyJD",
    task_items=[
        TaskItem(
            instruction="在首页中搜索iPhone 15，并查看搜索结果的第一个商品。",
            verify_func=validate_task_one,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将首页中的商品iPhone 15 任意颜色 128GB加入购物车。",
            verify_func=validate_task_two,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="立即购买首页中一台任意规格的iPhone 15。",
            verify_func=validate_task_three,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="计算一下我购物车中电子产品的总价是多少。",
            verify_func=validate_task_four,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="首页显示的前十个商品中的手机商品的总价是多少。",
            verify_func=validate_task_five,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="结算我的第一个待付款订单。",
            verify_func=validate_task_six,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='给Apple产品京东自营旗舰店发消息问"什么时候发货"。',
            verify_func=validate_task_seven,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="计算首页展示的商品中前十个有多少个是手机。",
            verify_func=validate_task_eight,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="计算购物车中所有商品的总价。",
            verify_func=validate_task_nine,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="计算待收货的订单有多少项。",
            verify_func=validate_task_ten,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="计算我一共收到多少条京东客服的消息。",
            verify_func=validate_task_eleven,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看京东秒送的消息，确定商品还有多久能送达。",
            verify_func=validate_task_twelve,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="算一下首页前十个商品中，评分大于等于4.7的有几个。",
            verify_func=validate_task_thirteen,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看首页iPhone15商品页共有多少条评论。",
            verify_func=validate_task_fourteen,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='将商品"iPhone 15 蓝色 128GB 1件"、"iPhone 15 黑色 256GB 2件"、"iPhone 15 粉色 128GB 3件"共6件商品加入购物车。',
            verify_func=validate_task_fifteen,
            human_steps=16,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="将购物车的iPhone15买下来，满3000减50的优惠券结算。",
            verify_func=validate_task_sixteen,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='进入首页iPhone15商品详情并进入店铺主页，然后立即购买店铺中"iPhone 15 粉色 256GB 1件"。',
            verify_func=validate_task_seventeen,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="取消我的nike鞋的待付款订单。",
            verify_func=validate_task_eighteen,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='新建默认地址"代嘉仪，13066666666，文秀街9号"。',
            verify_func=validate_task_nineteen,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="设置Apple产品京东自营旗舰店的聊天为消息免打扰。",
            verify_func=validate_task_twenty,
            human_steps=4,
            is_reasoning=False,
        ),
    ],
)
