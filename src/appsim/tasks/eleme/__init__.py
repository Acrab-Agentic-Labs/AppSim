# 引用所有检验函数
from ..base import AppTasks, NumericReasoningCategory, TaskItem

# 导入所有验证函数（按指令序号对应 eval_1 至 eval_40）
from .eval_1 import TASK1_ANSWER_SCHEMA, verify_coupon_total_value
from .eval_2 import TASK2_ANSWER_SCHEMA, verify_highest_sales_among_top_rated_restaurants
from .eval_3 import TASK3_ANSWER_SCHEMA, verify_lowest_priced_featured_drink
from .eval_4 import TASK4_ANSWER_SCHEMA, verify_saved_address_recipient_count
from .eval_5 import TASK5_ANSWER_SCHEMA, verify_latest_order_status
from .eval_6 import verify_search_price_filter_applied
from .eval_7 import verify_unaccepted_order_canceled
from .eval_8 import verify_automatic_payment_enabled
from .eval_9 import verify_cart_items_ordered
from .eval_10 import verify_phone_edit_page_opened
from .eval_11 import verify_system_notifications_disabled
from .eval_12 import verify_coupon_applied_order_completed
from .eval_13 import verify_delivery_driver_contacted
from .eval_14 import verify_restaurant_shared_with_contact
from .eval_15 import verify_shipping_address_added
from .eval_16 import verify_order_issue_refund_requested
from .eval_17 import verify_distance_sorted_restaurant_order_completed
from .eval_18 import verify_scheduled_order_completed
from .eval_19 import TASK19_ANSWER_SCHEMA, verify_monthly_spending_amount
from .eval_20 import verify_latest_review_deleted
from .eval_21 import verify_order_insurance_claim_requested
from .eval_22 import verify_two_scheduled_orders_completed
from .eval_23 import TASK23_ANSWER_SCHEMA, verify_latest_delivered_order_paid_amount
from .eval_24 import verify_search_history_cleared
from .eval_25 import TASK25_ANSWER_SCHEMA, verify_weekly_category_spending_amount
from .eval_26 import TASK26_ANSWER_SCHEMA, verify_peak_ordering_period_and_share
from .eval_27 import TASK27_ANSWER_SCHEMA, verify_free_delivery_restaurant_count
from .eval_28 import TASK28_ANSWER_SCHEMA, verify_recent_order_recipient_count
from .eval_29 import TASK29_ANSWER_SCHEMA, verify_high_sales_restaurant_count
from .eval_30 import TASK30_ANSWER_SCHEMA, verify_recent_order_delivery_person_count
from .eval_31 import TASK31_ANSWER_SCHEMA, verify_monthly_order_count
from .eval_32 import TASK32_ANSWER_SCHEMA, verify_weekly_cuisine_spending_amount
from .eval_33 import TASK33_ANSWER_SCHEMA, verify_largest_available_coupon
from .eval_34 import TASK34_ANSWER_SCHEMA, verify_store_coupon_count
from .eval_35 import TASK35_ANSWER_SCHEMA, verify_highest_spending_restaurant
from .eval_36 import TASK36_ANSWER_SCHEMA, verify_low_delivery_threshold_restaurant_count
from .eval_37 import TASK37_ANSWER_SCHEMA, verify_nearest_recommended_restaurant_name
from .eval_38 import TASK38_ANSWER_SCHEMA, verify_top_selling_breakfast_item
from .eval_39 import TASK39_ANSWER_SCHEMA, verify_nearest_low_cost_drink_restaurant
from .eval_40 import TASK40_ANSWER_SCHEMA, verify_fastest_drink_restaurant_delivery

# 所有测试指令列表（共40条，instruct 完全匹配需求描述）
ELEME_TASKS = AppTasks(
    package_name="com.example.eleme_sim",
    task_items=[
        TaskItem(
            instruction="看看红包卡券里的红包还能帮我省多少钱，计算红包的总价值",
            verify_func=verify_coupon_total_value,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='在"美食外卖"下，商家好评最高的10家店中，月销量最高的店铺名为？"。',
            verify_func=verify_highest_sales_among_top_rated_restaurants,
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="帮我看看瑞幸咖啡的招牌系列中，价格最低的一款饮品叫什么名字。",
            verify_func=verify_lowest_priced_featured_drink,
            human_steps=8,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK3_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看已保存的地址信息中，于骁的信息有几个。",
            verify_func=verify_saved_address_recipient_count,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK4_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看最近一个订单的状态。",
            verify_func=verify_latest_order_status,
            human_steps=2,
            evaluation_type="answer",
            answer_schema=TASK5_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='搜索"烤鸡"，价格区间"0-30"。',
            verify_func=verify_search_price_filter_applied,
            human_steps=7,
        ),
        TaskItem(
            instruction="帮我检查我刚买的炸酱面的订单商家接单没有？如果没接单就帮我取消订单。",
            verify_func=verify_unaccepted_order_canceled,
            human_steps=5,
        ),
        TaskItem(
            instruction="开启支付宝免密支付。",
            verify_func=verify_automatic_payment_enabled,
            human_steps=4,
        ),
        TaskItem(
            instruction="把购物车里面的这几道菜都一起下单，地址选择默认。",
            verify_func=verify_cart_items_ordered,
            human_steps=4,
        ),
        TaskItem(
            instruction="进入修改手机号的页面，然后停留在这个页面。",
            verify_func=verify_phone_edit_page_opened,
            human_steps=3,
        ),
        TaskItem(
            instruction="关闭系统消息通知。",
            verify_func=verify_system_notifications_disabled,
            human_steps=6,
        ),
        TaskItem(
            instruction='搜索"肯德基"，选择任意套餐，使用第一张优惠券，完成下单。',
            verify_func=verify_coupon_applied_order_completed,
            human_steps=11,
        ),
        TaskItem(
            instruction='找到第一个配送中的订单，联系骑手，问"出了什么情况，怎么还没到"。',
            verify_func=verify_delivery_driver_contacted,
            human_steps=8,
        ),
        TaskItem(
            instruction="找到麻辣烫订单，把商家主页分享给微信好友。",
            verify_func=verify_restaurant_shared_with_contact,
            human_steps=7,
        ),
        TaskItem(
            instruction="添加地址为华中师范大学元宝山学生公寓二期，姓名于骁，手机号13022222222，标签选择学校，门牌号613。",
            verify_func=verify_shipping_address_added,
            human_steps=15,
        ),
        TaskItem(
            instruction='跟刚送到的订单的商家说"缺少可乐，要求退款"。',
            verify_func=verify_order_issue_refund_requested,
            human_steps=9,
        ),
        TaskItem(
            instruction='在"美食外卖"排"距离优先"的商家，随便下单任意一家的任意一个商品。',
            verify_func=verify_distance_sorted_restaurant_order_completed,
            human_steps=7,
        ),
        TaskItem(
            instruction='在"美食外卖"选有"跨天预订"的商家，然后下单第一家第一个商品，地址默认，选择明天中午（11-13点)时间段。',
            verify_func=verify_scheduled_order_completed,
            human_steps=12,
        ),
        TaskItem(
            instruction="找一下我的账单，看一下我9月花销多少钱。",
            verify_func=verify_monthly_spending_amount,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK19_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="找到已评价的评价，删除最近的一个评价。",
            verify_func=verify_latest_review_deleted,
            human_steps=5,
        ),
        TaskItem(
            instruction="找到有麻辣烫的订单，申请食无忧理赔。",
            verify_func=verify_order_insurance_claim_requested,
            human_steps=6,
        ),
        TaskItem(
            instruction='进入"美食外卖"，找有食无忧和跨天预订的商家列表，找第一个商家给于骁和余味两个人分别下一单明日中午11-13点到达的热销商品，于骁的地址用任意一个，余味的地址用唯一的一个。',
            verify_func=verify_two_scheduled_orders_completed,
            human_steps=25,
        ),
        TaskItem(
            instruction="找到最新的已送达订单，进入订单详情页，查看实付多少元。",
            verify_func=verify_latest_delivered_order_paid_amount,
            human_steps=4,
            evaluation_type="answer",
            answer_schema=TASK23_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="清除搜索历史。",
            verify_func=verify_search_history_cleared,
            human_steps=3,
        ),
        TaskItem(
            instruction="找一下我的账单，看看（10.13-10.19）这周买韩国料理花了多少钱。",
            verify_func=verify_weekly_category_spending_amount,
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK25_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="找一下我的账单的月账单，看看我9月在哪个时间段点外卖次数最多，占比是多少（用小数表示）。",
            verify_func=verify_peak_ordering_period_and_share,
            human_steps=5,
            numeric_reasoning_categories=[
                NumericReasoningCategory.CALCULATE,
                NumericReasoningCategory.COMPARE_SELECT,
            ],
            evaluation_type="answer",
            answer_schema=TASK26_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="饿了么首页推荐的前十家店铺，免配送费的有几家？",
            verify_func=verify_free_delivery_restaurant_count,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK27_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看一下订单里面前五个订单，有几个订单的收货人是于骁。",
            verify_func=verify_recent_order_recipient_count,
            human_steps=19,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK28_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看一下首页推荐的前20个商家中，月销量超过4000的有几家。",
            verify_func=verify_high_sales_restaurant_count,
            human_steps=4,
            numeric_reasoning_categories=[
                NumericReasoningCategory.COUNT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="answer",
            answer_schema=TASK29_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看一下我订单里面前五个订单，有几个订单是周丹奎送的。",
            verify_func=verify_recent_order_delivery_person_count,
            human_steps=19,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK30_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看一下我十月点了多少次外卖。",
            verify_func=verify_monthly_order_count,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK31_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看一下周账单吃湘菜花了多少钱。",
            verify_func=verify_weekly_cuisine_spending_amount,
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK32_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看下我能用的最大的红包是多少。",
            verify_func=verify_largest_available_coupon,
            human_steps=5,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK33_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看下指定瑞幸能用的券有几张。",
            verify_func=verify_store_coupon_count,
            human_steps=5,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK34_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看下账单中九月我消费最多的商家",
            verify_func=verify_highest_spending_restaurant,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK35_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看下首页推荐店铺的前20家中，起送费低于30元的有几家。",
            verify_func=verify_low_delivery_threshold_restaurant_count,
            human_steps=4,
            numeric_reasoning_categories=[
                NumericReasoningCategory.COUNT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="answer",
            answer_schema=TASK36_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="看下首页推荐店铺的前23家中，距离我最近的店铺的名字叫什么。",
            verify_func=verify_nearest_recommended_restaurant_name,
            human_steps=5,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK37_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="粤式早茶所有商品销量最高的是哪个。",
            verify_func=verify_top_selling_breakfast_item,
            human_steps=10,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK38_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="主页推荐店铺的前20家中，哪个饮品店配送费加起送费最低且离我最近。",
            verify_func=verify_nearest_low_cost_drink_restaurant,
            human_steps=4,
            numeric_reasoning_categories=[
                NumericReasoningCategory.CALCULATE,
                NumericReasoningCategory.COMPARE_SELECT,
            ],
            evaluation_type="answer",
            answer_schema=TASK39_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="主页推荐店铺的前20家中，哪个饮品店送达最快。",
            verify_func=verify_fastest_drink_restaurant_delivery,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK40_ANSWER_SCHEMA,
        ),
    ],
)
