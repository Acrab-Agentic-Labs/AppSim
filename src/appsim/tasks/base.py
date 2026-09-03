# -*- coding:utf-8 -*-
from enum import Enum
from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


class NumericReasoningCategory(str, Enum):
    """数值推理任务分类。"""

    COUNT = "count"
    CALCULATE = "calculate"
    COMPARE_SELECT = "compare_select"
    THRESHOLD_FILTER = "threshold_filter"


class TaskItem(BaseModel):
    """任务项数据结构

    Attributes:
        instruction: 任务指令描述（字符串）
        verify_func: 验证函数，接受一个字典参数
    """

    instruction: str
    verify_func: Callable[[dict], Any]
    human_steps: int
    evaluation_type: Literal["state", "answer", "hybrid"] = "state"
    answer_schema: Optional[Dict[str, Any]] = None
    numeric_reasoning_categories: List[NumericReasoningCategory] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True


class AppTasks(BaseModel):
    """应用任务数据结构

    Attributes:
        package_name: App的包名
        task_items: 该App所有的TaskItem列表
    """

    package_name: str
    task_items: List[TaskItem]
