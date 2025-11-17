# 引用所有检验函数
from ..base import TaskItem, AppTasks

# 导入所有验证函数（按指令序号对应 .eval_1 至 .eval_35）
from .eval_1 import check_click_hotel
from .eval_2 import check_click_flight
from .eval_3 import check_click_train
from .eval_4 import check_click_message
from .eval_5 import check_click_itinerary
from .eval_6 import check_click_profile
from .eval_7 import check_hotel_search_chengdu
from .eval_8 import check_hotel_search_dates
from .eval_9 import check_hotel_search_guests
from .eval_10 import check_flight_search_gz_sz
from .eval_11 import check_flight_search_date
from .eval_12 import check_flight_search_cabin
from .eval_13 import check_train_search_bj_sh
from .eval_14 import check_train_search_date
from .eval_15 import check_train_search_student
from .eval_16 import check_hotel_search_beijing
from .eval_17 import check_hotel_search_shanghai
from .eval_18 import check_flight_search_bj_sz
from .eval_19 import check_flight_search_cd_sh_first
from .eval_20 import check_train_search_bj_sh_date
from .eval_21 import check_train_search_cs_tj_student
from .eval_22 import check_hotel_search_beijing_top3_avg_price
from .eval_23 import check_hotel_search_shanghai_min_price
from .eval_24 import check_flight_search_price_avg
from .eval_25 import check_train_search_max_price
from .eval_26 import check_booking_hotel_shanghai
from .eval_27 import check_booking_flight_wh_sz
from .eval_28 import check_booking_train_bj_sh
from .eval_29 import check_booking_hotel_cheapest
from .eval_30 import check_booking_train_time
from .eval_31 import check_booking_multi_step
from .eval_32 import check_booking_complex_budget
from .eval_33 import check_booking_batch_train
from .eval_34 import check_booking_complex_batch
from .eval_35 import check_booking_batch_flight

# 所有测试指令列表（共35条，与上述导入函数一一对应）
CTRIP_TASKS = AppTasks(
    package_name="com.example.Ctrip",
    task_items=[
        TaskItem(
            instruction="进入酒店预订。",
            verify_func=check_click_hotel,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入机票预订。",
            verify_func=check_click_flight,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="看一下火车票预订。",
            verify_func=check_click_train,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="看一下消息列表。",
            verify_func=check_click_message,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="看看我的行程。",
            verify_func=check_click_itinerary,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="进入我的页面。",
            verify_func=check_click_profile,
            human_steps=1,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="给我看看上海的酒店列表。",
            verify_func=check_hotel_search_chengdu,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="帮我找入住时间10月20日，退房时间10月21日的酒店列表。",
            verify_func=check_hotel_search_dates,
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="帮我找间数1、成人数1、儿童数1，的酒店列表。",
            verify_func=check_hotel_search_guests,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='帮我找出发地 "广州"、目的地 "深圳"的航班列表。',
            verify_func=check_flight_search_gz_sz,
            human_steps=6,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找出日期10月22日的航班列表。",
            verify_func=check_flight_search_date,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找出公务/头等舱的航班列表。",
            verify_func=check_flight_search_cabin,
            human_steps=3,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='找出发地 "北京"、目的地 "上海"的火车车次列表。',
            verify_func=check_train_search_bj_sh,
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找到日期10月24日的火车车次列表。",
            verify_func=check_train_search_date,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找到能用学生票的车次列表。",
            verify_func=check_train_search_student,
            human_steps=4,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找出入住时间10月22日，退房时间10月23日的北京酒店列表。",
            verify_func=check_hotel_search_beijing,
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找出入住时间今天，退房时间明天，间数2，成人数2，儿童数0的上海酒店列表。",
            verify_func=check_hotel_search_shanghai,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="出发地北京，目的地深圳，10月25号，看看有啥航班。",
            verify_func=check_flight_search_bj_sz,
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='出发地 "成都"、目的地 "上海"，10月20号，头等舱，看看有什么航班。',
            verify_func=check_flight_search_cd_sh_first,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='出发地 "北京"、目的地 "上海"，10月22日，看看有什么车次。',
            verify_func=check_train_search_bj_sh_date,
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='出发地 "杭州"、目的地 "深圳"，10月24日，学生票，看看有什么车次。',
            verify_func=check_train_search_cs_tj_student,
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="帮我筛选北京评分最高的前 3 家酒店的平均价。",
            verify_func=check_hotel_search_beijing_top3_avg_price,
            human_steps=5,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="帮我检索上海所有酒店中最低的价格。",
            verify_func=check_hotel_search_shanghai_min_price,
            human_steps=7,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查10月21日从北京飞广州的机票，统计下最便宜的 3 趟航班的平均价格告诉我。",
            verify_func=check_flight_search_price_avg,
            human_steps=11,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="查10月22日广州到杭州下午2点到5点的车次，算下这些车次中最高的价格。",
            verify_func=check_train_search_max_price,
            human_steps=13,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="找10月22日到10月25日上海住的酒店，客房数和入住人数默认，点第一个酒店，第一个房型预订。",
            verify_func=check_booking_hotel_shanghai,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='出发地 "成都"、目的地 "深圳"，10月24号，舱型默认，预订第一架航班。',
            verify_func=check_booking_flight_wh_sz,
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='出发地 "北京"、目的地 "上海"，10月23日，预订第一班车次。',
            verify_func=check_booking_train_bj_sh,
            human_steps=13,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="找上海的10月21日到10月25日的酒店，客房数和入住人数默认，选择价格最低的酒店，最便宜的房型预订。",
            verify_func=check_booking_hotel_cheapest,
            human_steps=17,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='出发地 "北京"、目的地 "上海"，10月20日，预订下午1点到下午3点的任意一班车次。',
            verify_func=check_booking_train_time,
            human_steps=14,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="先订北京飞上海的机票（10月20日，经济舱），再订上海的酒店（入住10月20日，退房10月21日），最后订上海回北京的火车票（10月21日）。",
            verify_func=check_booking_multi_step,
            human_steps=36,
            is_reasoning=False,
        ),
        TaskItem(
            instruction='订10月20日从杭州到北京的最快火车票（5小时内达），住北京王府井希尔顿酒店两晚（10.20-10.22），再订10.22北京回杭州的高铁，计算所有费用后判断 2000 元够不够。请直接回答"够"或"不够"',
            verify_func=check_booking_complex_budget,
            human_steps=50,
            is_reasoning=True,
        ),
        TaskItem(
            instruction="订5张10月20日深圳到北京的火车票，5小时内到达。",
            verify_func=check_booking_batch_train,
            human_steps=32,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="订5张10月20日广州到北京的火车票，再订北京 3 家不同的酒店。",
            verify_func=check_booking_complex_batch,
            human_steps=61,
            is_reasoning=False,
        ),
        TaskItem(
            instruction="订10月25日北京飞上海的6张经济舱机票。",
            verify_func=check_booking_batch_flight,
            human_steps=42,
            is_reasoning=False,
        ),
    ],
)
