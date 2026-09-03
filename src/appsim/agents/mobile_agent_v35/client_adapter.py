# -*- coding: utf-8 -*-
"""为官方 GUIOwlWrapper 注入 AppSim 所需的请求默认值。"""

from __future__ import annotations

from typing import Any, Callable

from openai import OpenAI


class _CompletionsWithDefaults:
    def __init__(self, completions: Any, max_tokens: int) -> None:
        self._completions = completions
        self._max_tokens = max_tokens

    def create(self, *args: Any, **kwargs: Any) -> Any:
        kwargs.setdefault("max_tokens", self._max_tokens)
        return self._completions.create(*args, **kwargs)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._completions, name)


class _ChatWithDefaults:
    def __init__(self, chat: Any, max_tokens: int) -> None:
        self._chat = chat
        self.completions = _CompletionsWithDefaults(
            chat.completions,
            max_tokens,
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self._chat, name)


class OpenAIClientWithDefaults:
    """代理 OpenAI 客户端，并为 Chat Completions 补齐默认参数。"""

    def __init__(self, client: Any, max_tokens: int) -> None:
        if max_tokens <= 0:
            raise ValueError("max_tokens 必须为正整数")
        self._client = client
        self.chat = _ChatWithDefaults(client.chat, max_tokens)

    def close(self) -> None:
        self._client.close()

    def __getattr__(self, name: str) -> Any:
        return getattr(self._client, name)


def configure_official_wrapper_client(
    wrapper: Any,
    api_key: str,
    api_base: str,
    max_tokens: int,
    timeout_seconds: float,
    client_factory: Callable[..., Any] = OpenAI,
) -> None:
    """替换官方 wrapper 的客户端，不复制或修改官方推理逻辑。"""

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds 必须大于 0")

    previous_client = getattr(wrapper, "bot", None)
    if previous_client is not None and hasattr(previous_client, "close"):
        previous_client.close()

    client = client_factory(
        api_key=api_key,
        base_url=api_base,
        timeout=timeout_seconds,
    )
    wrapper.bot = OpenAIClientWithDefaults(client, max_tokens)


__all__ = [
    "OpenAIClientWithDefaults",
    "configure_official_wrapper_client",
]
