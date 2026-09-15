"""V-Droid verifier 与动作补全 LLM 客户端。"""

import json
import logging
import math
import urllib.error
import urllib.request
from typing import Any, Optional

from openai import OpenAI


class VDroidInfrastructureError(RuntimeError):
    """需要由 AppSim runner 重试的外部服务错误。"""


def _base_url(endpoint: str) -> str:
    normalized = endpoint.rstrip("/")
    for suffix in ("/score", "/health"):
        if normalized.endswith(suffix):
            return normalized[: -len(suffix)]
    return normalized


class VerifierClient:
    """调用已部署的 V-Droid `/score` 服务。"""

    def __init__(
        self,
        endpoint: str,
        timeout_seconds: float = 300.0,
        max_batch_size: int = 64,
    ):
        if not endpoint:
            raise ValueError("V-Droid verifier endpoint 不能为空")
        if timeout_seconds <= 0:
            raise ValueError("verifier timeout 必须大于 0")
        if max_batch_size <= 0:
            raise ValueError("verifier batch size 必须大于 0")
        self.base_url = _base_url(endpoint)
        self.timeout_seconds = timeout_seconds
        self.max_batch_size = max_batch_size

    def _request_json(
        self,
        path: str,
        payload: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        data = None
        headers: dict[str, str] = {}
        method = "GET"
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
            method = "POST"
        request = urllib.request.Request(
            f"{self.base_url}{path}",
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(
                request,
                timeout=self.timeout_seconds,
            ) as response:
                result = json.load(response)
        except urllib.error.HTTPError as error:
            detail = error.read().decode("utf-8", "replace")
            raise VDroidInfrastructureError(
                f"V-Droid verifier HTTP {error.code}: {detail}"
            ) from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise VDroidInfrastructureError(
                f"无法连接 V-Droid verifier {self.base_url}: {error}"
            ) from error
        if not isinstance(result, dict):
            raise VDroidInfrastructureError(f"V-Droid verifier 返回格式错误: {result!r}")
        return result

    def check_health(self) -> dict[str, Any]:
        """检查 verifier 是否已加载。"""

        result = self._request_json("/health")
        if result.get("status") != "ok":
            raise VDroidInfrastructureError(f"V-Droid verifier 未就绪: {result}")
        return result

    def score(self, prompts: list[str]) -> list[float]:
        """分批评分并保持输入顺序。"""

        if not prompts:
            raise ValueError("prompts 不能为空")
        scores: list[float] = []
        for start in range(0, len(prompts), self.max_batch_size):
            batch = prompts[start : start + self.max_batch_size]
            result = self._request_json("/score", {"prompts": batch})
            batch_scores = result.get("scores")
            if not isinstance(batch_scores, list) or len(batch_scores) != len(batch):
                raise VDroidInfrastructureError(
                    f"V-Droid verifier 评分数量错误: expected={len(batch)} actual={batch_scores!r}"
                )
            for score in batch_scores:
                if not isinstance(score, (int, float)) or not math.isfinite(score):
                    raise VDroidInfrastructureError(f"V-Droid verifier 返回无效评分: {score!r}")
                scores.append(float(score))
        return scores


class HelperLLMClient:
    """调用 OpenAI 兼容文本模型补全动作参数。"""

    def __init__(
        self,
        api_key: str,
        api_base: str,
        model_name: str,
        timeout_seconds: float = 300.0,
        max_tokens: int = 512,
    ):
        if not api_key or not api_base or not model_name:
            raise ValueError("V-Droid helper LLM 的 API key、base URL 和 model name 均不能为空")
        if timeout_seconds <= 0 or max_tokens <= 0:
            raise ValueError("helper timeout 和 max_tokens 必须大于 0")
        self.model_name = model_name
        self.max_tokens = max_tokens
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("openai._base_client").setLevel(logging.WARNING)
        normalized_api_base = api_base.rstrip("/")
        self.api_mode = (
            "responses" if normalized_api_base.endswith("/responses") else "chat"
        )
        if self.api_mode == "responses":
            normalized_api_base = normalized_api_base[: -len("/responses")]
        self.client = OpenAI(
            api_key=api_key,
            base_url=normalized_api_base,
            timeout=timeout_seconds,
            max_retries=0,
        )

    @staticmethod
    def _response_text(response: Any) -> str:
        if not response.choices:
            return ""
        content = response.choices[0].message.content
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = []
            for item in content:
                text = item.get("text") if isinstance(item, dict) else getattr(item, "text", None)
                if text:
                    parts.append(str(text))
            return "\n".join(parts).strip()
        return ""

    def complete_action(self, prompt: str) -> tuple[str, Any]:
        """补全一个含占位符的候选动作。"""

        try:
            if self.api_mode == "responses":
                response = self.client.responses.create(
                    model=self.model_name,
                    input=prompt,
                    max_output_tokens=self.max_tokens,
                )
                text = str(getattr(response, "output_text", "") or "").strip()
            else:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.0,
                    max_tokens=self.max_tokens,
                )
                text = self._response_text(response)
        except Exception as error:
            status_code = getattr(error, "status_code", None)
            error_summary = type(error).__name__
            if status_code is not None:
                error_summary += f"(status={status_code})"
            raise VDroidInfrastructureError(
                f"V-Droid helper LLM 调用失败: {error_summary}"
            ) from error
        if not text:
            raise VDroidInfrastructureError("V-Droid helper LLM 返回空内容")
        return text, response

    def close(self) -> None:
        self.client.close()
