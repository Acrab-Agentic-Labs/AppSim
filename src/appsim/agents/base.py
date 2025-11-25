# -*- coding:utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class AgentExecutionResult(BaseModel):
    """Agent 执行结果数据结构

    Attributes:
        success: 是否成功执行
        completed_steps: 完成的步骤数
        total_actions: 总动作数
        executed_actions: 已执行的动作列表
        screenshot_dir: 截图目录
        screenshots: 截图路径列表
        final_message: 最终消息（可选）
        error: 错误信息（可选）
    """

    success: bool
    completed_steps: int
    total_actions: int
    executed_actions: List[Dict[str, Any]]
    screenshot_dir: str
    screenshots: List[str]
    error: Optional[str] = None
    final_message: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True


class BaseAgent(ABC):
    """Agent基类接口

    所有Agent实现类都应该继承此类，并实现execute_instruction方法
    """

    @abstractmethod
    def reset(self) -> None:
        """重置 Agent"""
        pass

    @abstractmethod
    def execute_instruction(self, *args, **kwargs) -> AgentExecutionResult:
        """执行指令

        Args:
            *args: 位置参数，不做限制
            **kwargs: 关键字参数，不做限制

        Returns:
            ExecutionResult: 执行结果，包含success、completed_steps、total_actions、
                           executed_actions、screenshots、error等字段
        """
        pass
