# -*- coding:utf-8 -*-
import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI

from .answer_extractor import AnswerExtractor, ExtractionResult
from .schema_utils import extract_first_json_object, schema_to_prompt, validate_and_normalize


SYSTEM_PROMPT = """你是一个答案结构化提取器。

你的任务是：将 agent 针对用户任务指令的回复（final_message）按照给定 JSON Schema 结构化为一个 JSON 对象。

说明：
- final_message 是 agent 对用户任务指令的回复，但格式可能不符合 JSON Schema 要求
- 你需要理解任务指令的意图，将 final_message 中的回答内容按 schema 重新组织输出

输出格式要求：
- 直接输出裸 JSON 对象，不要使用 markdown 代码块包裹
- 不要在 JSON 前后添加任何解释、前缀或后缀文本

字段填写规则：
- schema 中的必填字段（required）必须存在于输出中，不得遗漏 key
- 字段值必须从 final_message 中提取，不要臆造不存在的信息
- 如果 final_message 中无法找到某字段的依据，该字段填 null
- 如果 final_message 为空或与任务无关，所有字段填 null
"""


class BaselineExtractor(AnswerExtractor):
    """基于 OpenAI-compatible 接口的 baseline 答案提取器。"""

    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        api_base: Optional[str] = None,
        model_name: Optional[str] = None,
    ) -> None:
        self.api_key = api_key or os.getenv("ANSWER_EXTRACTOR_API_KEY") or os.getenv("API_KEY")
        self.api_base = api_base or os.getenv("ANSWER_EXTRACTOR_API_BASE") or os.getenv("API_BASE")
        self.model_name = model_name or os.getenv("ANSWER_EXTRACTOR_MODEL_NAME") or os.getenv("MODEL_NAME")

        if not self.api_key:
            raise ValueError("缺少 ANSWER_EXTRACTOR_API_KEY 或 API_KEY")
        if not self.model_name:
            raise ValueError("缺少 ANSWER_EXTRACTOR_MODEL_NAME 或 MODEL_NAME")

        client_kwargs: Dict[str, Any] = {"api_key": self.api_key}
        if self.api_base:
            client_kwargs["base_url"] = self.api_base
        self.client = OpenAI(**client_kwargs)

    def _build_user_prompt(
        self,
        *,
        instruction: str,
        final_message: Optional[str],
        answer_schema: Dict[str, Any],
    ) -> str:
        final_message_text = str(final_message).strip() if final_message else "（无内容）"
        return (
            f"任务指令:\n{instruction}\n\n"
            f"Agent final_message:\n{final_message_text}\n\n"
            f"目标 JSON Schema:\n{schema_to_prompt(answer_schema)}"
        )

    def _call_llm(self, user_prompt: str) -> str:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                temperature=0.0,
                response_format={"type": "json_object"},
                messages=messages,
            )
        except Exception:
            response = self.client.chat.completions.create(
                model=self.model_name,
                temperature=0.0,
                messages=messages,
            )
        return response.choices[0].message.content or ""

    def extract(
        self,
        *,
        final_message: Optional[str],
        answer_schema: Dict[str, Any],
        instruction: str,
    ) -> ExtractionResult:
        try:
            user_prompt = self._build_user_prompt(
                instruction=instruction,
                final_message=final_message,
                answer_schema=answer_schema,
            )
            model_output = self._call_llm(user_prompt)
            raw_answer = extract_first_json_object(model_output)
            normalized_answer, errors = validate_and_normalize(raw_answer, answer_schema)
            if errors:
                return ExtractionResult(
                    success=False,
                    no_canonicalize_answer=raw_answer,
                    answer=normalized_answer,
                    error="; ".join(errors),
                )
            return ExtractionResult(
                success=True,
                no_canonicalize_answer=raw_answer,
                answer=normalized_answer,
                error=None,
            )
        except Exception as exc:
            return ExtractionResult(
                success=False,
                no_canonicalize_answer=None,
                answer=None,
                error=str(exc),
            )
