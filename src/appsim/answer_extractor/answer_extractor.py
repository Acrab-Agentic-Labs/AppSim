# -*- coding:utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from pydantic import BaseModel


class ExtractionResult(BaseModel):
    """答案提取结果。

    Attributes:
        success: 提取是否成功
        no_canonicalize_answer: 未做 canonicalization 的结构化答案
        answer: 经过轻量 canonicalization 后的最终答案
        error: 错误信息
    """

    success: bool
    no_canonicalize_answer: Any = None
    answer: Any = None
    error: Optional[str] = None


class AnswerExtractor(ABC):
    """答案提取器抽象接口。"""

    @abstractmethod
    def extract(
        self,
        *,
        final_message: Optional[str],
        answer_schema: Dict[str, Any],
        instruction: str,
    ) -> ExtractionResult:
        """从 final_message 中提取结构化答案。"""
        raise NotImplementedError
