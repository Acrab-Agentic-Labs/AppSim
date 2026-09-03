# 引用所有检验函数
from ..base import AppTasks, NumericReasoningCategory, TaskItem

# 导入所有验证函数（按指令序号对应 .eval_1 至 .eval_35）
from .eval_1 import verify_hotel_booking_page_opened
from .eval_2 import verify_flight_booking_page_opened
from .eval_3 import verify_train_booking_page_opened
from .eval_4 import verify_message_list_opened
from .eval_5 import verify_itinerary_page_opened
from .eval_6 import verify_profile_page_opened
from .eval_7 import verify_hotel_search_results_for_requested_location
from .eval_8 import verify_hotel_search_results_for_requested_dates
from .eval_9 import verify_hotel_search_results_for_requested_guest_counts
from .eval_10 import verify_flight_search_results_for_requested_route
from .eval_11 import verify_flight_search_results_for_requested_date
from .eval_12 import verify_flight_search_results_for_requested_cabin
from .eval_13 import verify_train_search_results_for_requested_route
from .eval_14 import verify_train_search_results_for_requested_date
from .eval_15 import verify_student_ticket_train_search_results
from .eval_16 import verify_hotel_search_results_for_location_and_dates
from .eval_17 import verify_hotel_search_results_for_guest_counts_and_dates
from .eval_18 import verify_flight_search_results_for_route_and_date
from .eval_19 import verify_first_class_flight_search_results
from .eval_20 import verify_train_search_results_for_route_and_date
from .eval_21 import verify_student_train_search_results_for_route_and_date
from .eval_22 import TASK22_ANSWER_SCHEMA, verify_top_rated_hotel_average_price
from .eval_23 import TASK23_ANSWER_SCHEMA, verify_lowest_hotel_price
from .eval_24 import TASK24_ANSWER_SCHEMA, verify_cheapest_flight_average_price
from .eval_25 import TASK25_ANSWER_SCHEMA, verify_highest_train_fare
from .eval_26 import verify_first_hotel_room_booking_created
from .eval_27 import verify_first_flight_booking_created
from .eval_28 import verify_first_train_booking_created
from .eval_29 import verify_cheapest_hotel_room_booking_created
from .eval_30 import verify_train_booking_for_requested_time
from .eval_31 import verify_multi_segment_trip_bookings_created
from .eval_32 import TASK32_ANSWER_SCHEMA, verify_multi_segment_trip_budget_sufficiency
from .eval_33 import verify_batch_train_tickets_booked
from .eval_34 import verify_batch_hotel_bookings_created
from .eval_35 import verify_batch_flight_tickets_booked

# 所有测试指令列表（共35条，与上述导入函数一一对应）
CTRIP_TASKS = AppTasks(
    package_name="com.example.ctrip_sim",
    task_items=[
        TaskItem(
            instruction="进入酒店预订。",
            verify_func=verify_hotel_booking_page_opened,
            human_steps=1,
        ),
        TaskItem(
            instruction="进入机票预订。",
            verify_func=verify_flight_booking_page_opened,
            human_steps=1,
        ),
        TaskItem(
            instruction="看一下火车票预订。",
            verify_func=verify_train_booking_page_opened,
            human_steps=1,
        ),
        TaskItem(
            instruction="看一下消息列表。",
            verify_func=verify_message_list_opened,
            human_steps=1,
        ),
        TaskItem(
            instruction="看看我的行程。",
            verify_func=verify_itinerary_page_opened,
            human_steps=1,
        ),
        TaskItem(
            instruction="进入我的页面。",
            verify_func=verify_profile_page_opened,
            human_steps=1,
        ),
        TaskItem(
            instruction="给我看看上海的酒店列表。",
            verify_func=verify_hotel_search_results_for_requested_location,
            human_steps=4,
        ),
        TaskItem(
            instruction="帮我找入住时间10月20日，退房时间10月21日的酒店列表。",
            verify_func=verify_hotel_search_results_for_requested_dates,
            human_steps=2,
        ),
        TaskItem(
            instruction="帮我找间数1、成人数1、儿童数1，的酒店列表。",
            verify_func=verify_hotel_search_results_for_requested_guest_counts,
            human_steps=4,
        ),
        TaskItem(
            instruction='帮我找出发地 "广州"、目的地 "深圳"的航班列表。',
            verify_func=verify_flight_search_results_for_requested_route,
            human_steps=6,
        ),
        TaskItem(
            instruction="找出日期10月22日的航班列表。",
            verify_func=verify_flight_search_results_for_requested_date,
            human_steps=4,
        ),
        TaskItem(
            instruction="找出公务/头等舱的航班列表。",
            verify_func=verify_flight_search_results_for_requested_cabin,
            human_steps=3,
        ),
        TaskItem(
            instruction='找出发地 "北京"、目的地 "上海"的火车车次列表。',
            verify_func=verify_train_search_results_for_requested_route,
            human_steps=7,
        ),
        TaskItem(
            instruction="找到日期10月24日的火车车次列表。",
            verify_func=verify_train_search_results_for_requested_date,
            human_steps=5,
        ),
        TaskItem(
            instruction="找到能用学生票的车次列表。",
            verify_func=verify_student_ticket_train_search_results,
            human_steps=4,
        ),
        TaskItem(
            instruction="找出入住时间10月22日，退房时间10月23日的北京酒店列表。",
            verify_func=verify_hotel_search_results_for_location_and_dates,
            human_steps=5,
        ),
        TaskItem(
            instruction="找出入住时间今天，退房时间明天，间数2，成人数2，儿童数0的上海酒店列表。",
            verify_func=verify_hotel_search_results_for_guest_counts_and_dates,
            human_steps=8,
        ),
        TaskItem(
            instruction="出发地北京，目的地深圳，10月25号，看看有啥航班。",
            verify_func=verify_flight_search_results_for_route_and_date,
            human_steps=8,
        ),
        TaskItem(
            instruction='出发地 "成都"、目的地 "上海"，10月20号，头等舱，看看有什么航班。',
            verify_func=verify_first_class_flight_search_results,
            human_steps=9,
        ),
        TaskItem(
            instruction='出发地 "北京"、目的地 "上海"，10月22日，看看有什么车次。',
            verify_func=verify_train_search_results_for_route_and_date,
            human_steps=9,
        ),
        TaskItem(
            instruction='出发地 "杭州"、目的地 "深圳"，10月24日，学生票，看看有什么车次。',
            verify_func=verify_student_train_search_results_for_route_and_date,
            human_steps=10,
        ),
        TaskItem(
            instruction="帮我计算北京评分最高的前 3 家酒店的平均价。",
            verify_func=verify_top_rated_hotel_average_price,
            human_steps=5,
            numeric_reasoning_categories=[
                NumericReasoningCategory.CALCULATE,
                NumericReasoningCategory.COMPARE_SELECT,
            ],
            evaluation_type="answer",
            answer_schema=TASK22_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="帮我检索上海所有酒店中最低的价格。",
            verify_func=verify_lowest_hotel_price,
            human_steps=7,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
            evaluation_type="answer",
            answer_schema=TASK23_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查10月21日从北京飞广州的机票，统计下最便宜的 3 趟航班的平均价格告诉我。",
            verify_func=verify_cheapest_flight_average_price,
            human_steps=11,
            numeric_reasoning_categories=[
                NumericReasoningCategory.CALCULATE,
                NumericReasoningCategory.COMPARE_SELECT,
            ],
            evaluation_type="answer",
            answer_schema=TASK24_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="查10月22日广州到杭州下午2点到5点的车次，算下这些车次中最高的价格。",
            verify_func=verify_highest_train_fare,
            human_steps=13,
            numeric_reasoning_categories=[
                NumericReasoningCategory.COMPARE_SELECT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="answer",
            answer_schema=TASK25_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="找10月22日到10月25日上海住的酒店，客房数和入住人数默认，点第一个酒店，第一个房型预订。",
            verify_func=verify_first_hotel_room_booking_created,
            human_steps=14,
        ),
        TaskItem(
            instruction='出发地 "成都"、目的地 "深圳"，10月24号，舱型默认，预订第一架航班。',
            verify_func=verify_first_flight_booking_created,
            human_steps=12,
        ),
        TaskItem(
            instruction='出发地 "北京"、目的地 "上海"，10月23日，预订第一班车次。',
            verify_func=verify_first_train_booking_created,
            human_steps=13,
        ),
        TaskItem(
            instruction="找上海的10月21日到10月25日的酒店，客房数和入住人数默认，选择价格最低的酒店，最便宜的房型预订。",
            verify_func=verify_cheapest_hotel_room_booking_created,
            human_steps=17,
            numeric_reasoning_categories=[NumericReasoningCategory.COMPARE_SELECT],
        ),
        TaskItem(
            instruction='出发地 "北京"、目的地 "上海"，10月20日，预订下午1点到下午3点的任意一班车次。',
            verify_func=verify_train_booking_for_requested_time,
            human_steps=14,
            numeric_reasoning_categories=[NumericReasoningCategory.THRESHOLD_FILTER],
        ),
        TaskItem(
            instruction="先订北京飞上海的机票（10月20日，经济舱），再订上海的酒店（入住10月20日，退房10月21日），最后订上海回北京的火车票（10月21日）。",
            verify_func=verify_multi_segment_trip_bookings_created,
            human_steps=36,
        ),
        TaskItem(
            instruction='订10月20日从杭州到北京的最快火车票（5小时内达），住北京王府井希尔顿酒店两晚（10.20-10.22），再订10.22北京回杭州的火车，计算所有费用后判断 2000 元够不够。请直接回答"够"或"不够"',
            verify_func=verify_multi_segment_trip_budget_sufficiency,
            human_steps=50,
            numeric_reasoning_categories=[
                NumericReasoningCategory.CALCULATE,
                NumericReasoningCategory.COMPARE_SELECT,
                NumericReasoningCategory.THRESHOLD_FILTER,
            ],
            evaluation_type="answer",
            answer_schema=TASK32_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction="订5张10月20日深圳到北京的火车票，5小时内到达。",
            verify_func=verify_batch_train_tickets_booked,
            human_steps=32,
            numeric_reasoning_categories=[NumericReasoningCategory.THRESHOLD_FILTER],
        ),
        TaskItem(
            instruction="订5张10月20日广州到北京的火车票，再订北京 3 家不同的酒店。",
            verify_func=verify_batch_hotel_bookings_created,
            human_steps=61,
        ),
        TaskItem(
            instruction="订10月25日北京飞上海的6张经济舱机票。",
            verify_func=verify_batch_flight_tickets_booked,
            human_steps=42,
        ),
    ],
)
