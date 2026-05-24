# -*- coding:utf-8 -*-
from typing import Any, Callable, Dict, List, Literal, Optional

from pydantic import BaseModel


class TaskItem(BaseModel):
    """任务项数据结构

    Attributes:
        instruction: 任务指令描述（字符串）
        verify_func: 验证函数，接受一个字典参数
    """

    instruction: str
    verify_func: Callable[[dict], Any]
    human_steps: int
    is_reasoning: bool
    evaluation_type: Literal["state", "answer", "hybrid"] = "state"
    answer_schema: Optional[Dict[str, Any]] = None

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
