# 引用所有检验函数
from ..base import AppTasks, TaskItem

# 导入所有验证函数（按指令序号对应 eval_1 至 eval_30）
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

# 所有测试指令列表（共40条，instruct 完全匹配需求描述）
ELEME_TASKS = AppTasks(
    package_name="com.example.eleme_sim",
    task_items=[
        TaskItem(
            instruction="看看红包卡券里的红包还能帮我省多少钱，计算红包的总价值",
            verify_func=validate_task_one,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='在"美食外卖"下，商家好评最高的10家店中，月销量最高的店铺名为？"。',
            verify_func=validate_task_two,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="帮我看看瑞幸咖啡的招牌系列中，价格最低的一款饮品叫什么名字。",
            verify_func=validate_task_three,
            human_steps=8,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看已保存的地址信息中，于骁的信息有几个。",
            verify_func=validate_task_four,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查看最近一个订单的状态。",
            verify_func=validate_task_five,
            human_steps=2,
            is_reasoning=True,
        ),
        TaskItem(
            instruction='搜索"烤鸡"，价格区间"0-30"。',
            verify_func=validate_task_six,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="帮我检查我刚买的炸酱面的订单商家接单没有？如果没接单就帮我取消订单。",
            verify_func=validate_task_seven,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="开启支付宝免密支付。",
            verify_func=validate_task_eight,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="把购物车里面的这几道菜都一起下单，地址选择默认。",
            verify_func=validate_task_nine,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入修改手机号的页面，然后停留在这个页面。",
            verify_func=validate_task_ten,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="关闭系统消息通知。",
            verify_func=validate_task_eleven,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='搜索"肯德基"，选择任意套餐，使用第一张优惠券，完成下单。',
            verify_func=validate_task_twelve,
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='找到第一个配送中的订单，联系骑手，问"出了什么情况，怎么还没到"。',
            verify_func=validate_task_thirteen,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找到麻辣烫订单，把商家主页分享给微信好友。",
            verify_func=validate_task_fourteen,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="添加地址为华中师范大学元宝山学生公寓二期，姓名于骁，手机号13022222222，标签选择学校，门牌号613。",
            verify_func=validate_task_fifteen,
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='跟刚送到的订单的商家说"缺少可乐，要求退款"。',
            verify_func=validate_task_sixteen,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='在"美食外卖"排"距离优先"的商家，随便下单任意一家的任意一个商品。',
            verify_func=validate_task_seventeen,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='在"美食外卖"选有"跨天预订"的商家，然后下单第一家第一个商品，地址默认，选择明天中午（11-13点)时间段。',
            verify_func=validate_task_eighteen,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找一下我的账单，看一下我9月花销多少钱。",
            verify_func=validate_task_nineteen,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="找到已评价的评价，删除最近的一个评价。",
            verify_func=validate_task_twenty,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找到有麻辣烫的订单，申请食无忧理赔。",
            verify_func=validate_task_twenty_one,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='进入"美食外卖"，找有食无忧和跨天预订的商家列表，找第一个商家给于骁和余味两个人分别下一单明日中午11-13点到达的热销商品，于骁的地址用任意一个，余味的地址用唯一的一个。',
            verify_func=validate_task_twenty_two,
            human_steps=25,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找到最新的已送达订单，进入订单详情页，查看实付多少元。",
            verify_func=validate_task_twenty_three,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="清除搜索历史。",
            verify_func=validate_task_twenty_four,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找一下我的账单，看看（10.13-10.19）这周买韩国料理花了多少钱。",
            verify_func=validate_task_twenty_five,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="找一下我的账单的月账单，看看我9月在哪个时间段点外卖次数最多，占比是多少（用小数表示）。",
            verify_func=validate_task_twenty_six,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="饿了么首页推荐的前十家店铺，免配送费的有几家？",
            verify_func=validate_task_twenty_seven,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看一下订单里面前五个订单，有几个订单的收货人是于骁。",
            verify_func=validate_task_twenty_eight,
            human_steps=19,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看一下首页推荐的前20个商家中，月销量超过4000的有几家。",
            verify_func=validate_task_twenty_nine,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看一下我订单里面前五个订单，有几个订单是周丹奎送的。",
            verify_func=validate_task_thirty,
            human_steps=19,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看一下我十月点了多少次外卖。",
            verify_func=validate_task_thirty_one,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看一下周账单吃湘菜花了多少钱。",
            verify_func=validate_task_thirty_two,
            human_steps=3,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看下我能用的最大的红包是多少。",
            verify_func=validate_task_thirty_three,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看下指定瑞幸能用的券有几张。",
            verify_func=validate_task_thirty_four,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看下账单中九月我消费最多的商家",
            verify_func=validate_task_thirty_five,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看下首页推荐店铺的前20家中，起送费低于30元的有几家。",
            verify_func=validate_task_thirty_six,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="看下首页推荐店铺的前23家中，距离我最近的店铺的名字叫什么。",
            verify_func=validate_task_thirty_seven,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="粤式早茶所有商品销量最高的是哪个。",
            verify_func=validate_task_thirty_eight,
            human_steps=10,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="主页推荐店铺的前20家中，哪个饮品店配送费加起送费最低且离我最近。",
            verify_func=validate_task_thirty_nine,
            human_steps=4,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="主页推荐店铺的前20家中，哪个饮品店送达最快。",
            verify_func=validate_task_forty,
            human_steps=4,
            is_reasoning=True,
        ),
    ],
)
