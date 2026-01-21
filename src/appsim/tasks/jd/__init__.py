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
from .eval_21 import validate_task_twenty_one
from .eval_22 import validate_task_twenty_two
from .eval_23 import validate_task_twenty_three
from .eval_24 import validate_task_twenty_four
from .eval_25 import validate_task_twenty_five
from .eval_26 import validate_task_twenty_six
from .eval_27 import validate_task_twenty_seven
from .eval_28 import validate_task_twenty_eight
from .eval_29 import validate_task_twenty_nine
from .eval_30 import validate_task_thirty
from .eval_31 import validate_task_thirty_one
from .eval_32 import validate_task_thirty_two
from .eval_33 import validate_task_thirty_three
from .eval_34 import validate_task_thirty_four
from .eval_35 import validate_task_thirty_five
from .eval_36 import validate_task_thirty_six
from .eval_37 import validate_task_thirty_seven
from .eval_38 import validate_task_thirty_eight
from .eval_39 import validate_task_thirty_nine
from .eval_40 import validate_task_forty

JD_TASKS = AppTasks(
    package_name="com.example.jd_sim",
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
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="立即购买首页中一台任意规格的iPhone 15。",
            verify_func=validate_task_three,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="计算一下我购物车中电子产品的总价是多少。",
            verify_func=validate_task_four,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="首页显示的前十个商品中的手机商品的总价是多少。",
            verify_func=validate_task_five,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="结算我的第一个待付款订单后再确认收货。",
            verify_func=validate_task_six,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="给Apple官方旗舰店发消息问手机什么时候发货。",
            verify_func=validate_task_seven,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="计算首页展示的商品中前十个有多少个是手机，给出一个阿拉伯数字即可。",
            verify_func=validate_task_eight,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="计算购物车中所有商品的总价。",
            verify_func=validate_task_nine,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="计算待收货的订单有多少项，给出一个阿拉伯数字即可。",
            verify_func=validate_task_ten,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="计算我一共收到多少条京东客服的消息，给出一个阿拉伯数字即可。",
            verify_func=validate_task_eleven,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看京东秒送的物流消息，确定商品还有多少分钟能送达,给出一个阿拉伯数字即可。",
            verify_func=validate_task_twelve,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="算一下首页全部商品中，评分大于等于4.7的有几个，给出一个阿拉伯数字即可。",
            verify_func=validate_task_thirteen,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看首页前十个商品中华为商品评论数最多的为多少条，给出一个阿拉伯数字即可。",
            verify_func=validate_task_fourteen,
            human_steps=8,
            is_reasoning=False,
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
            instruction='帮我在Apple京东自营店购买一件iPhone 15 粉色 256GB"。',
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
            instruction="设置Apple官方旗舰店的聊天为消息免打扰。",
            verify_func=validate_task_twenty,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="在Apple官方旗舰店筛选出价格在6000.0至8000.0的手机类别商品有多少个，给出一个阿拉伯数字即可。",
            verify_func=validate_task_twenty_one,
            human_steps=9,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看评价iPhone15电池续航强的评论有多少,给出一个阿拉伯数字即可。",
            verify_func=validate_task_twenty_two,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="计算Apple官方旗舰店评分大于4.7的商品的平均价格，保留一位小数。",
            verify_func=validate_task_twenty_three,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看我的订单中，待使用的电子产品共有多少件，给出一个阿拉伯数字即可。",
            verify_func=validate_task_twenty_four,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="统计首页前10个商品中不是手机商品的平均评分,保留2位小数。",
            verify_func=validate_task_twenty_five,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="统计待使用的京东超市的订单总价，保留一位小数。",
            verify_func=validate_task_twenty_six,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="找到我的待收货订单中购买件数最多的商品并确认收货。",
            verify_func=validate_task_twenty_seven,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="找到购物车中单价最低的商品购买5件。",
            verify_func=validate_task_twenty_eight,
            human_steps=6,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="结算总价低于2000的所有待付款订单。",
            verify_func=validate_task_twenty_nine,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="进入Apple官方旗舰店选择价格最高的商品规格加入购物车并结算，选择赵六的地址。",
            verify_func=validate_task_thirty,
            human_steps=15,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看购物车中所有商品，将价格最高的三件商品移出购物车。",
            verify_func=validate_task_thirty_one,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="找到首页前十个商品中价格最低的手机，选择其最便宜的规格购买。",
            verify_func=validate_task_thirty_two,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="比较Apple官方旗舰店和华为官方旗舰店的粉丝数，告诉我粉丝量更高的店铺名。",
            verify_func=validate_task_thirty_three,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="将陈七地址详情中的电话号码改成18972746987。",
            verify_func=validate_task_thirty_four,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入华为官方旗舰店选择评分最高的商品加入购物车并结算，选择李四的地址。",
            verify_func=validate_task_thirty_five,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="将首页所有华为手机商品的最小的内存版本加入购物车。",
            verify_func=validate_task_thirty_six,
            human_steps=14,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="购买首页前十个商品中买家评价最多的华为商品。",
            verify_func=validate_task_thirty_seven,
            human_steps=15,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="搜索“华为”，筛选出起价在4500到5000的手机加入购物车并结算，送到王五的地址。",
            verify_func=validate_task_thirty_eight,
            human_steps=17,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="选择首页联想电脑中价格最高规格立即购买，送到张三的地址。",
            verify_func=validate_task_thirty_nine,
            human_steps=12,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="找到首页前十个商品中评分为4.7的电子商品，选择他们价格最高的规格加入购物车。",
            verify_func=validate_task_forty,
            human_steps=15,
            is_reasoning=True,
        ),
    ],
)
