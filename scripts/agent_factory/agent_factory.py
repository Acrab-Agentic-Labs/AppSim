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
    OPEN_SOURCE_UI_TRAS = "OpenSource-UI-TRAS"
    MOBILE_AGENT_V35 = "MobileAgent-v3.5"
    V_DROID = "V-Droid"
    M3A_AGENT = "m3a_agent"


def create_agent(
    agent_name: AgentEnum,
    device_id: str,
    screenshots_dir: str = "screenshots",
    app_package: str = "",
) -> BaseAgent:
    """
    创建 Agent 实例

    Args:
        agent_name: Agent 类型（AgentEnum）
        device_id: 设备 ID（必需）
        screenshots_dir: 截图保存目录（可选，默认 "screenshots"）
        app_package: 当前评测 App 包名（MobileAgent-v3.5 必需）

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

    elif agent_name == AgentEnum.OPEN_SOURCE_UI_TRAS:
        from appsim.agents.open_source_ui_tras import OpenSourceUITRASAgent

        api_key = os.getenv("OPEN_SOURCE_UI_TRAS_API_KEY", api_key) or "EMPTY"
        base_url = os.getenv("OPEN_SOURCE_UI_TRAS_API_BASE", base_url)
        model_name = (
            os.getenv(
                "OPEN_SOURCE_UI_TRAS_MODEL_NAME",
                model_name,
            )
            or "OpenSource-UI-TRAS"
        )
        max_tokens = int(os.getenv("OPEN_SOURCE_UI_TRAS_MAX_TOKENS", "400"))
        history_turns = int(os.getenv("OPEN_SOURCE_UI_TRAS_HISTORY_TURNS", "8"))
        thought_language = os.getenv(
            "OPEN_SOURCE_UI_TRAS_THOUGHT_LANGUAGE",
            "English",
        )
        request_timeout_seconds = float(os.getenv("OPEN_SOURCE_UI_TRAS_REQUEST_TIMEOUT_SECONDS", "300"))
        default_code_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "ModelRepos",
                "UI-TARS",
                "codes",
            )
        )
        official_code_dir = os.getenv(
            "OPEN_SOURCE_UI_TRAS_CODE_DIR",
            default_code_dir,
        )

        return OpenSourceUITRASAgent(
            model_name=model_name,
            api_key=api_key,
            api_base=base_url,
            device_id=device_id,
            official_code_dir=official_code_dir,
            screenshots_dir=screenshots_dir,
            max_tokens=max_tokens,
            history_turns=history_turns,
            thought_language=thought_language,
            request_timeout_seconds=request_timeout_seconds,
            model_kwargs={},
        )

    elif agent_name == AgentEnum.MOBILE_AGENT_V35:
        from appsim.agents.mobile_agent_v35 import MobileAgentV35Agent

        if not app_package:
            raise ValueError("MobileAgent-v3.5 requires app_package")

        api_key = os.getenv("MOBILE_AGENT_V35_API_KEY", api_key) or "EMPTY"
        base_url = os.getenv("MOBILE_AGENT_V35_API_BASE", base_url)
        model_name = (
            os.getenv(
                "MOBILE_AGENT_V35_MODEL_NAME",
                model_name,
            )
            or "GUI-Owl-1.5-8B-Instruct"
        )
        max_steps = int(os.getenv("MOBILE_AGENT_V35_MAX_STEPS", "50"))
        max_tokens = int(os.getenv("MOBILE_AGENT_V35_MAX_TOKENS", "512"))
        request_timeout_seconds = float(os.getenv("MOBILE_AGENT_V35_REQUEST_TIMEOUT_SECONDS", "300"))
        wait_after_action_seconds = float(os.getenv("MOBILE_AGENT_V35_WAIT_AFTER_ACTION_SECONDS", "3"))
        default_code_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "ModelRepos",
                "MobileAgent",
                "Mobile-Agent-v3.5",
                "android_world_v3.5",
            )
        )
        official_code_dir = os.getenv(
            "MOBILE_AGENT_V35_CODE_DIR",
            default_code_dir,
        )

        return MobileAgentV35Agent(
            model_name=model_name,
            api_key=api_key,
            api_base=base_url,
            device_id=device_id,
            app_package=app_package,
            official_code_dir=official_code_dir,
            screenshots_dir=screenshots_dir,
            max_steps=max_steps,
            max_tokens=max_tokens,
            request_timeout_seconds=request_timeout_seconds,
            wait_after_action_seconds=wait_after_action_seconds,
        )

    elif agent_name == AgentEnum.V_DROID:
        from appsim.agents.vdroid import VDroidAgent

        verifier_api_base = os.getenv("VDROID_VERIFIER_API_BASE", base_url)
        helper_api_base = os.getenv("VDROID_HELPER_API_BASE")
        helper_api_key = os.getenv("VDROID_HELPER_API_KEY")
        helper_model_name = os.getenv("VDROID_HELPER_MODEL_NAME")
        if not verifier_api_base:
            raise ValueError("V-Droid requires VDROID_VERIFIER_API_BASE or API_BASE")
        if not helper_api_base or not helper_api_key or not helper_model_name:
            raise ValueError(
                "V-Droid requires VDROID_HELPER_API_BASE, "
                "VDROID_HELPER_API_KEY and VDROID_HELPER_MODEL_NAME"
            )

        default_code_dir = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "..",
                "..",
                "ModelRepos",
                "V-Droid",
            )
        )
        return VDroidAgent(
            verifier_api_base=verifier_api_base,
            helper_api_key=helper_api_key,
            helper_api_base=helper_api_base,
            helper_model_name=helper_model_name,
            device_id=device_id,
            official_code_dir=os.getenv("VDROID_CODE_DIR", default_code_dir),
            screenshots_dir=screenshots_dir,
            max_steps=int(os.getenv("VDROID_MAX_STEPS", "50")),
            max_action_completion_attempts=int(
                os.getenv("VDROID_ACTION_COMPLETION_ATTEMPTS", "3")
            ),
            wait_after_action_seconds=float(
                os.getenv("VDROID_WAIT_AFTER_ACTION_SECONDS", "2")
            ),
            verifier_timeout_seconds=float(
                os.getenv("VDROID_VERIFIER_TIMEOUT_SECONDS", "300")
            ),
            helper_timeout_seconds=float(
                os.getenv("VDROID_HELPER_TIMEOUT_SECONDS", "300")
            ),
            helper_max_tokens=int(os.getenv("VDROID_HELPER_MAX_TOKENS", "512")),
            verifier_batch_size=int(os.getenv("VDROID_VERIFIER_BATCH_SIZE", "64")),
            summary_mode=os.getenv("VDROID_SUMMARY_MODE", "llm"),
            history_turns=int(os.getenv("VDROID_HISTORY_TURNS", "20")),
            allow_app_switch=os.getenv("VDROID_ALLOW_APP_SWITCH", "0").lower()
            in {"1", "true", "yes"},
            stagnation_limit=int(os.getenv("VDROID_STAGNATION_LIMIT", "50")),
            review_terminal_actions=os.getenv(
                "VDROID_REVIEW_TERMINAL_ACTIONS", "1"
            ).lower()
            in {"1", "true", "yes"},
            device_connect_attempts=int(
                os.getenv("VDROID_DEVICE_CONNECT_ATTEMPTS", "3")
            ),
            device_connect_retry_seconds=float(
                os.getenv("VDROID_DEVICE_CONNECT_RETRY_SECONDS", "2")
            ),
        )

    raise ValueError(f"无效的 Agent 名称: {agent_name}")
