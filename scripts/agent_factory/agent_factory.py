# -*- coding: utf-8 -*-
"""Agent Factory - 统一的 Agent 构造函数"""

import os
from enum import Enum

from appsim.agents.base import BaseAgent


class AgentEnum(Enum):
    """Agent 类型枚举"""

    SEED15_VL = "Seed-1.5-VL"
    UI_TARS_15 = "UI-TARS-1.5"
    GPT5 = "GPT-5"
    GEMINI25_PRO = "Gemini-2.5-Pro"
    CLAUDE45_SONNET = "Claude-4.5-Sonnet"
    QWEN3_VL = "Qwen3-VL"
    AGENTCPM_GUI = "AgentCPM-GUI"
    M3A_AGENT = "m3a_agent"


def create_agent(
        agent_name: AgentEnum,
        device_id: str,
        screenshots_dir: str = "screenshots",
) -> BaseAgent:
    """
    创建 Agent 实例

    Args:
        agent_name: Agent 类型（AgentEnum）
        device_id: 设备 ID（必需）
        screenshots_dir: 截图保存目录（可选，默认 "screenshots"）

    Returns:
        BaseAgent: Agent 实例

    Raises:
        ValueError: 如果 agent_name 无效或缺少必要的环境变量
    """
    # 从环境变量读取API配置
    api_key = os.getenv("API_KEY")
    base_url = os.getenv("API_BASE")
    model_name = os.getenv("MODEL_NAME")

    def _create_m3a_agent(selected_api_key: str, selected_base_url: str, selected_model_name: str) -> BaseAgent:
        from appsim.agents.m3a_agent import M3AAgent

        return M3AAgent(
            api_key=selected_api_key,
            base_url=selected_base_url,
            model_name=selected_model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs={},
        )

    if agent_name == AgentEnum.SEED15_VL:
        # 导入模型
        from appsim.agents.seed_agent import SeedAgent

        # 获取特定环境变量配置
        api_key = os.getenv("SEED15_VL_API_KEY", api_key)
        base_url = os.getenv("SEED15_VL_API_BASE", base_url)
        model_name = os.getenv("SEED15_VL_MODEL_NAME", model_name)

        # 超参
        model_kwargs = {"temperature": 0.0, "top_p": 0.7}

        return SeedAgent(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == AgentEnum.UI_TARS_15:
        # 导入模型
        from appsim.agents.seed_agent import SeedAgent

        # 获取特定环境变量配置
        api_key = os.getenv("UI_TARS_15_API_KEY", api_key)
        base_url = os.getenv("UI_TARS_15_API_BASE", base_url)
        model_name = os.getenv("UI_TARS_15_MODEL_NAME", model_name)
        # 超参
        model_kwargs = {"temperature": 0.0, "top_p": 0.7}

        return SeedAgent(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == AgentEnum.M3A_AGENT:
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == AgentEnum.GPT5:
        api_key = os.getenv("GPT5_API_KEY", api_key)
        base_url = os.getenv("GPT5_API_BASE", base_url)
        model_name = os.getenv("GPT5_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == AgentEnum.GEMINI25_PRO:
        api_key = os.getenv("GEMINI25_PRO_API_KEY", api_key)
        base_url = os.getenv("GEMINI25_PRO_API_BASE", base_url)
        model_name = os.getenv("GEMINI25_PRO_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == AgentEnum.CLAUDE45_SONNET:
        api_key = os.getenv("CLAUDE45_SONNET_API_KEY", api_key)
        base_url = os.getenv("CLAUDE45_SONNET_API_BASE", base_url)
        model_name = os.getenv("CLAUDE45_SONNET_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == AgentEnum.QWEN3_VL:
        # 导入模型
        from appsim.agents.qwen3 import Qwen3Agent

        # 获取特定环境变量配置
        api_key = os.getenv("QWEN3_VL_API_KEY", api_key)
        base_url = os.getenv("QWEN3_VL_API_BASE", base_url)
        model_name = os.getenv("QWEN3_VL_MODEL_NAME", model_name)
        # 超参
        model_kwargs = {}

        return Qwen3Agent(
            model_name=model_name,
            api_key=api_key,
            api_base=base_url,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == AgentEnum.AGENTCPM_GUI:
        # 导入模型
        from appsim.agents.agentcpm import AgentCPMAgent

        # 获取特定环境变量配置
        api_key = os.getenv("AGENTCPM_GUI_API_KEY", api_key) or "EMPTY"
        base_url = os.getenv("AGENTCPM_GUI_API_BASE", base_url)
        model_name = os.getenv("AGENTCPM_GUI_MODEL_NAME", model_name) or "AgentCPM-GUI"
        max_tokens = int(os.getenv("AGENTCPM_GUI_MAX_TOKENS", "512"))
        history_image_turns = int(os.getenv("AGENTCPM_GUI_HISTORY_IMAGE_TURNS", "1"))
        # 超参
        model_kwargs = {}

        return AgentCPMAgent(
            model_name=model_name,
            api_key=api_key,
            api_base=base_url,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            max_tokens=max_tokens,
            history_image_turns=history_image_turns,
            model_kwargs=model_kwargs,
        )

    raise ValueError(f"无效的 Agent 名称: {agent_name}")

