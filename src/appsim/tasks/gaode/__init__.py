# -*- coding:utf-8 -*-
from functools import wraps

from ..base import AppTasks, TaskItem
from .eval_1 import TASK1_ANSWER_SCHEMA, validate as validate_task_1
from .eval_2 import TASK2_ANSWER_SCHEMA, validate as validate_task_2
from .eval_3 import TASK3_ANSWER_SCHEMA, validate as validate_task_3
from .eval_4 import TASK4_ANSWER_SCHEMA, validate as validate_task_4
from .eval_5 import TASK5_ANSWER_SCHEMA, validate as validate_task_5
from .eval_6 import verify_modify_username
from .eval_7 import verify_navigate_to_destination
from .eval_8 import verify_open_bright_mode
from .eval_9 import verify_delete_recent_route
from .eval_10 import verify_favorite_nearest_restaurant
from .eval_11 import TASK11_ANSWER_SCHEMA, validate as validate_task_11
from .eval_12 import TASK12_ANSWER_SCHEMA, validate as validate_task_12
from .eval_13 import TASK13_ANSWER_SCHEMA, validate as validate_task_13
from .eval_14 import TASK14_ANSWER_SCHEMA, validate as validate_task_14
from .eval_15 import TASK15_ANSWER_SCHEMA, validate as validate_task_15
from .eval_16 import verify_walk_to_nearest_food
from .eval_17 import verify_navigate_from_poi
from .eval_18 import verify_add_waypoint
from .eval_19 import verify_call_top_attraction
from .eval_20 import verify_favorite_nearby_attractions
from .eval_21 import TASK21_ANSWER_SCHEMA, validate as validate_task_21
from .eval_22 import TASK22_ANSWER_SCHEMA, validate as validate_task_22
from .eval_23 import TASK23_ANSWER_SCHEMA, validate as validate_task_23
from .eval_24 import TASK24_ANSWER_SCHEMA, validate as validate_task_24
from .eval_25 import verify_cycle_to_favorite
from .eval_26 import verify_add_favorite_as_waypoint
from .eval_27 import verify_add_multiple_waypoints
from .eval_28 import verify_multi_stop_navigation


PACKAGE_NAME = "com.example.amap_sim"


_GAODE_SCOPE_GUIDANCE = "请只在当前高德/Amap模拟应用内完成任务，使用应用内置离线数据，不要打开系统设置或其它App。"


def _gaode_instruction(instruction: str) -> str:
    return f"{_GAODE_SCOPE_GUIDANCE}{instruction}"


def _wrap_device_only(verify_func):
    """Adapt ADB-based verifiers to the shared verify_func(device_id, **kwargs) API."""

    @wraps(verify_func)
    def wrapped(device_id=None, **kwargs):
        return verify_func(device_id=device_id)

    return wrapped


GAODE_TASKS = AppTasks(
    package_name=PACKAGE_NAME,
    task_items=[
        TaskItem(
            instruction=_gaode_instruction("进入周边界面，告诉我美食排行榜中评分最高的美食。"),
            verify_func=validate_task_1,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK1_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我第一次导航去了哪个地点。"),
            verify_func=validate_task_2,
            human_steps=2,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK2_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我账号的名字和id。"),
            verify_func=validate_task_3,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK3_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我周边最近的酒店名字。"),
            verify_func=validate_task_4,
            human_steps=4,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK4_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我收藏夹收藏了几个地点。"),
            verify_func=validate_task_5,
            human_steps=3,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK5_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("修改我的名字为123456。"),
            verify_func=_wrap_device_only(verify_modify_username),
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("步行导航去M+购物中心。"),
            verify_func=_wrap_device_only(verify_navigate_to_destination),
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("打开夜间模式。"),
            verify_func=_wrap_device_only(verify_open_bright_mode),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("删除最早的一次历史导航记录。"),
            verify_func=_wrap_device_only(verify_delete_recent_route),
            human_steps=2,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("收藏周边最近的餐馆。"),
            verify_func=_wrap_device_only(verify_favorite_nearest_restaurant),
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我步行去最近的酒店需要几分钟。"),
            verify_func=validate_task_11,
            human_steps=7,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK11_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我八七会议会址纪念馆的开放时间有几个小时。"),
            verify_func=validate_task_12,
            human_steps=5,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK12_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我M+购物中心的地址。"),
            verify_func=validate_task_13,
            human_steps=5,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK13_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我美食排行榜第一的地点的电话号码。"),
            verify_func=validate_task_14,
            human_steps=5,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK14_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我收藏的第一行饭店的名称。"),
            verify_func=validate_task_15,
            human_steps=6,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK15_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("步行导航去周边最近的美食店。"),
            verify_func=_wrap_device_only(verify_walk_to_nearest_food),
            human_steps=7,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("从M+购物中心导航到我的位置。"),
            verify_func=_wrap_device_only(verify_navigate_from_poi),
            human_steps=8,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("在导航去滨江饭店的路线中添加途经点群芳园，并且成功导航。"),
            verify_func=_wrap_device_only(verify_add_waypoint),
            human_steps=9,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("拨打周边景点排行榜第一的景点电话。"),
            verify_func=_wrap_device_only(verify_call_top_attraction),
            human_steps=5,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("收藏所有周边1km以内（包括1km）的所有景点。"),
            verify_func=_wrap_device_only(verify_favorite_nearby_attractions),
            human_steps=15,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我最近的一家四星级酒店名字（根据简介看）。"),
            verify_func=validate_task_21,
            human_steps=11,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK21_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我台北路公共停车场停车收费标准（一个小时多少钱）。"),
            verify_func=validate_task_22,
            human_steps=5,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK22_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我江汉大学（汉口校区）周边美食排行榜第一名是什么。"),
            verify_func=validate_task_23,
            human_steps=8,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK23_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("告诉我现在的位置，距离武汉市公安局（江岸分局）的周边美食排行榜第一名驾车��要几分钟。"),
            verify_func=validate_task_24,
            human_steps=9,
            is_reasoning=True,
            evaluation_type="answer",
            answer_schema=TASK24_ANSWER_SCHEMA,
        ),
        TaskItem(
            instruction=_gaode_instruction("骑行导航去我收藏的饭店中最近的一家。"),
            verify_func=_wrap_device_only(verify_cycle_to_favorite),
            human_steps=10,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("在导航去滨江饭店的路线中添加收藏中第一行地点作为途径点。"),
            verify_func=_wrap_device_only(verify_add_favorite_as_waypoint),
            human_steps=11,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction("在导航去M+购物中心的路线中添加第一个途经点芦苇滩，第二个途经点武汉市人民政府。"),
            verify_func=_wrap_device_only(verify_add_multiple_waypoints),
            human_steps=12,
            is_reasoning=False,
        ),
        TaskItem(
            instruction=_gaode_instruction('完成路线导航：M+购物中心到武汉市人民政府再到芦苇滩最后到我的位置的路线导航。'),
            verify_func=_wrap_device_only(verify_multi_stop_navigation),
            human_steps=13,
            is_reasoning=False,
        ),
    ],
)

# Backward-compatible alias for older local references.
AMAP_TASKS = GAODE_TASKS
