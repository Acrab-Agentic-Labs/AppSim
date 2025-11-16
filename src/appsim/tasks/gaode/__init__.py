# 引用所有检验函数
from ..base import TaskItem, AppTasks

from .eval_1 import verify_last_navigation_log1
from .eval_2 import verify_last_log2
from .eval_3 import verify_last_log3
from .eval_6 import verify_last_log6
from .eval_7 import verify_last_log7
from .eval_8 import verify_last_log8
from .eval_9 import verify_last_log9
from .eval_10 import verify_last_log10
from .eval_11 import verify_last_log11
from .eval_12 import verify_last_log12
from .eval_14 import verify_last_log14
from .eval_21 import eval_21
from .eval_22 import eval_22
from .eval_23 import eval_23
from .eval_24 import eval_24
from .eval_25 import eval_25
from .eval_26 import eval_26
from .eval_27 import eval_27
from .eval_28 import eval_28

# 所有指令
GAODE_TASKS = AppTasks(
    package_name="com.example.GaoDe",
    task_items=[
        TaskItem(instruction="我想看看有新消息吗", verify_func=verify_last_navigation_log1),
        TaskItem(instruction="我想去我收藏过的地点，请帮我选择一个", verify_func=verify_last_log2),
        TaskItem(instruction="搜搜附近的美食", verify_func=verify_last_log3),
        TaskItem(instruction="去和妈妈聊天", verify_func=verify_last_log6),
        TaskItem(instruction="我要导航回家", verify_func=verify_last_log7),
        TaskItem(instruction="想吃巴奴火锅，搜一搜在哪", verify_func=verify_last_log8),
        TaskItem(instruction="打车去东湖风景区", verify_func=verify_last_log9),
        TaskItem(instruction="预订汉庭酒店", verify_func=verify_last_log10),
        TaskItem(instruction="觉得老乡鸡不错，收藏这家餐厅", verify_func=verify_last_log11),
        TaskItem(instruction="想跟爸爸聊两句，发起和爸爸的聊天", verify_func=verify_last_log12),
        TaskItem(instruction="分享如家酒店位置给妈妈", verify_func=verify_last_log14),
        TaskItem(instruction="数一下我的订单数量", verify_func=eval_21),
        TaskItem(instruction="数一下我和妈妈的聊天记录条数", verify_func=eval_22),
        TaskItem(instruction="告诉我口碑最好的餐厅", verify_func=eval_23),
        TaskItem(instruction="正在营业的餐厅有几家", verify_func=eval_24),
        TaskItem(instruction="告诉我用时最短的景点", verify_func=eval_25),
        TaskItem(instruction="告诉我距离老象峰景区最近的机场", verify_func=eval_26),
        TaskItem(instruction="告诉我从我的位置途径如家酒店再到麦当劳用时最短的出行方式", verify_func=eval_27),
        TaskItem(instruction="告诉我到金雁酒店最优惠的优享型车名", verify_func=eval_28),
    ],
)

# 为了向后兼容，保留 ALL_INSTRUCTION
ALL_INSTRUCTION = [{"instruct": item.instruction, "fun": item.verify_func} for item in GAODE_TASKS.task_items]
