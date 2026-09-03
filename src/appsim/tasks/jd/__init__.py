from ..base import AppTasks, NumericReasoningCategory, TaskItem
from .eval_1 import verify_search_results_first_product_viewed
from .eval_2 import verify_product_added_to_cart
from .eval_3 import verify_immediate_product_purchase
from .eval_4 import verify_cart_electronics_total_price, TASK4_ANSWER_SCHEMA
from .eval_5 import verify_homepage_phone_products_total_price, TASK5_ANSWER_SCHEMA
from .eval_6 import verify_pending_order_settled_and_received
from .eval_7 import verify_store_message_sent
from .eval_8 import verify_homepage_phone_product_count, TASK8_ANSWER_SCHEMA
from .eval_9 import verify_cart_total_price, TASK9_ANSWER_SCHEMA
from .eval_10 import verify_pending_delivery_order_count, TASK10_ANSWER_SCHEMA
from .eval_11 import verify_customer_service_message_count, TASK11_ANSWER_SCHEMA
from .eval_12 import verify_delivery_eta_minutes, TASK12_ANSWER_SCHEMA
from .eval_13 import verify_high_rated_homepage_product_count, TASK13_ANSWER_SCHEMA
from .eval_14 import verify_product_review_count, TASK14_ANSWER_SCHEMA
from .eval_15 import verify_multiple_products_added_to_cart
from .eval_16 import verify_cart_purchase_with_discount_coupon
from .eval_17 import verify_store_product_purchased
from .eval_18 import verify_pending_order_cancelled
from .eval_19 import verify_default_address_created
from .eval_20 import verify_store_chat_muted
from .eval_21 import verify_filtered_product_count_by_price_range, TASK21_ANSWER_SCHEMA
from .eval_22 import verify_matching_product_review_count, TASK22_ANSWER_SCHEMA
from .eval_23 import verify_store_high_rated_product_average_price, TASK23_ANSWER_SCHEMA
from .eval_24 import verify_pending_electronics_item_count, TASK24_ANSWER_SCHEMA
from .eval_25 import verify_non_phone_product_average_rating, TASK25_ANSWER_SCHEMA
from .eval_26 import verify_store_pending_order_total_price, TASK26_ANSWER_SCHEMA
from .eval_27 import verify_highest_quantity_pending_order_confirmed
from .eval_28 import verify_lowest_price_cart_product_purchased
from .eval_29 import verify_low_value_pending_orders_settled
from .eval_30 import verify_highest_price_store_product_purchased
from .eval_31 import verify_most_expensive_cart_products_removed
from .eval_32 import verify_lowest_price_phone_product_purchased
from .eval_33 import verify_higher_follower_store_identified, TASK33_ANSWER_SCHEMA
from .eval_34 import verify_address_phone_number_updated
from .eval_35 import verify_highest_rated_store_product_purchased
from .eval_36 import verify_minimum_memory_phone_variants_added_to_cart
from .eval_37 import verify_most_reviewed_store_product_purchased
from .eval_38 import verify_filtered_phone_products_purchased
from .eval_39 import verify_highest_price_computer_product_purchased
from .eval_40 import verify_high_rated_electronic_products_added_to_cart

JD_TASKS = AppTasks(
    package_name="com.example.jd_sim",
    task_items=[
        TaskItem(
            instruction="在首页中搜索iPhone 15，并查看搜索结果的第一个商品。",
            verify_func=verify_search_results_first_product_viewed,
            human_steps=5,
        ),
        TaskItem(
            instruction="将首页中的商品iPhone 15 任意颜色 128GB加入购物车。",
            verify_func=verify_product_added_to_cart,
            human_steps=6,
        ),
        TaskItem(
            instruction="立即购买首页中一台任意规格的iPhone 15。",
            verify_func=verify_immediate_product_purchase,
            human_steps=4,
        ),
        TaskItem(
            instruction="计算一下我购物车中电子产品的总价是多少。",
            verify_func=verify_cart_electronics_total_price,
            human_steps=6,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK4_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="首页显示的前十个商品中的手机商品的总价是多少。",
            verify_func=verify_homepage_phone_products_total_price,
            human_steps=4,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK5_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="结算我的第一个待付款订单后再确认收货。",
            verify_func=verify_pending_order_settled_and_received,
            human_steps=6,
        ),
        TaskItem(
            instruction="给Apple官方旗舰店发消息问手机什么时候发货。",
            verify_func=verify_store_message_sent,
            human_steps=5,
        ),
        TaskItem(
            instruction="计算首页展示的商品中前十个有多少个是手机，给出一个阿拉伯数字即可。",
            verify_func=verify_homepage_phone_product_count,
            human_steps=2,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK8_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="计算购物车中所有商品的总价。",
            verify_func=verify_cart_total_price,
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK9_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="计算待收货的订单有多少项，给出一个阿拉伯数字即可。",
            verify_func=verify_pending_delivery_order_count,
            human_steps=7,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK10_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="计算我一共收到多少条京东客服的消息，给出一个阿拉伯数字即可。",
            verify_func=verify_customer_service_message_count,
            human_steps=3,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK11_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看京东秒送的物流消息，确定商品还有多少分钟能送达,给出一个阿拉伯数字即可。",
            verify_func=verify_delivery_eta_minutes,
            human_steps=4,
            evaluation_type="answer",
            answer_schema=TASK12_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="算一下首页全部商品中，评分大于等于4.7的有几个，给出一个阿拉伯数字即可。",
            verify_func=verify_high_rated_homepage_product_count,
            human_steps=6,
            numeric_reasoning_categories=[
                NumericReasoningCategory.COUNT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="answer",
            answer_schema=TASK13_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看首页前十个商品中华为商品评论数最多的为多少条，给出一个阿拉伯数字即可。",
            verify_func=verify_product_review_count,
            human_steps=8,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK14_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction='将商品"iPhone 15 蓝色 128GB 1件"、"iPhone 15 黑色 256GB 2件"、"iPhone 15 粉色 128GB 3件"共6件商品加入购物车。',
            verify_func=verify_multiple_products_added_to_cart,
            human_steps=16,
        ),
        TaskItem(
            instruction="将购物车的iPhone15买下来，满3000减50的优惠券结算。",
            verify_func=verify_cart_purchase_with_discount_coupon,
            human_steps=10,
        ),
        TaskItem(
            instruction='帮我在Apple京东自营店购买一件iPhone 15 粉色 256GB"。',
            verify_func=verify_store_product_purchased,
            human_steps=9,
        ),
        TaskItem(
            instruction="取消我的nike鞋的待付款订单。",
            verify_func=verify_pending_order_cancelled,
            human_steps=7,
        ),
        TaskItem(
            instruction='新建默认地址"代嘉仪，13066666666，文秀街9号"。',
            verify_func=verify_default_address_created,
            human_steps=12,
        ),
        TaskItem(
            instruction="设置Apple官方旗舰店的聊天为消息免打扰。",
            verify_func=verify_store_chat_muted,
            human_steps=4,
        ),
        TaskItem(
            instruction="在Apple官方旗舰店筛选出价格在6000.0至8000.0的手机类别商品有多少个，给出一个阿拉伯数字即可。",
            verify_func=verify_filtered_product_count_by_price_range,
            human_steps=9,
            numeric_reasoning_categories=[
                NumericReasoningCategory.COUNT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="answer",
            answer_schema=TASK21_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看评价iPhone15电池续航强的评论有多少,给出一个阿拉伯数字即可。",
            verify_func=verify_matching_product_review_count,
            human_steps=5,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK22_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="计算Apple官方旗舰店评分大于4.7的商品的平均价格，保留一位小数。",
            verify_func=verify_store_high_rated_product_average_price,
            human_steps=6,
            numeric_reasoning_categories=[
                NumericReasoningCategory.CALCULATE,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="answer",
            answer_schema=TASK23_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查看我的订单中，待使用的电子产品共有多少件，给出一个阿拉伯数字即可。",
            verify_func=verify_pending_electronics_item_count,
            human_steps=6,
            numeric_reasoning_categories=[NumericReasoningCategory.COUNT],
            evaluation_type="answer",
            answer_schema=TASK24_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="统计首页前10个商品中不是手机商品的平均评分,保留2位小数。",
            verify_func=verify_non_phone_product_average_rating,
            human_steps=7,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK25_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="统计待使用的京东超市的订单总价，保留一位小数。",
            verify_func=verify_store_pending_order_total_price,
            human_steps=6,
            numeric_reasoning_categories=[NumericReasoningCategory.CALCULATE],
            evaluation_type="answer",
            answer_schema=TASK26_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="找到我的待收货订单中购买件数最多的商品并确认收货。",
            verify_func=verify_highest_quantity_pending_order_confirmed,
            human_steps=6,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="找到购物车中单价最低的商品购买5件。",
            verify_func=verify_lowest_price_cart_product_purchased,
            human_steps=6,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="结算总价低于2000的所有待付款订单。",
            verify_func=verify_low_value_pending_orders_settled,
            human_steps=7,
            numeric_reasoning_categories=[NumericReasoningCategory.THRESHOLD_FILTER],
        ),
        TaskItem(
            instruction="进入Apple官方旗舰店选择价格最高的商品规格加入购物车并结算，选择赵六的地址。",
            verify_func=verify_highest_price_store_product_purchased,
            human_steps=15,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="查看购物车中所有商品，将价格最高的三件商品移出购物车。",
            verify_func=verify_most_expensive_cart_products_removed,
            human_steps=12,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="找到首页前十个商品中价格最低的手机，选择其最便宜的规格购买。",
            verify_func=verify_lowest_price_phone_product_purchased,
            human_steps=7,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="比较Apple官方旗舰店和华为官方旗舰店的粉丝数，直接告诉我粉丝量更高的店铺名。",
            verify_func=verify_higher_follower_store_identified,
            human_steps=8,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK33_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="将陈七地址详情中的电话号码改成18972746987。",
            verify_func=verify_address_phone_number_updated,
            human_steps=7,
        ),
        TaskItem(
            instruction="进入华为官方旗舰店选择评分最高的商品加入购物车并结算，选择李四的地址。",
            verify_func=verify_highest_rated_store_product_purchased,
            human_steps=12,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="将首页所有华为手机商品的最小的内存版本加入购物车。",
            verify_func=verify_minimum_memory_phone_variants_added_to_cart,
            human_steps=14,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="购买首页前十个商品中买家评价最多的华为商品。",
            verify_func=verify_most_reviewed_store_product_purchased,
            human_steps=15,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="搜索“华为”，筛选出起价在4500到5000的手机加入购物车并结算，送到王五的地址。",
            verify_func=verify_filtered_phone_products_purchased,
            human_steps=17,
            numeric_reasoning_categories=[NumericReasoningCategory.THRESHOLD_FILTER],
        ),
        TaskItem(
            instruction="选择首页联想电脑中价格最高规格立即购买，送到张三的地址。",
            verify_func=verify_highest_price_computer_product_purchased,
            human_steps=12,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction="找到首页前十个商品中评分为4.7的电子商品，选择他们价格最高的规格加入购物车。",
            verify_func=verify_high_rated_electronic_products_added_to_cart,
            human_steps=15,
            numeric_reasoning_categories=[
                NumericReasoningCategory.COMPARE_SELECT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
        ),
    ],
)
