# -*- coding: utf-8 -*-
"""Agent Factory - 统一的 Agent 构造函数"""

import os
from enum import Enum

from appsim.agents.base import BaseAgent


class BaselineEnum(Enum):
    """Baseline 模型类型枚举"""

    # ============ 论文中的19个模型 ============

    # Claude 系列 (使用 m3a_agent) - 论文中有4个
    CLAUDE_OPUS_47 = "Claude-Opus-4.7"
    CLAUDE_SONNET_46 = "Claude-Sonnet-4.6"
    CLAUDE_HAIKU_45 = "Claude-Haiku-4.5"
    CLAUDE_SONNET_45 = "Claude-Sonnet-4.5"

    # Gemini 系列 (使用 m3a_agent) - 论文中有3个
    GEMINI_3_PRO = "Gemini-3-Pro"
    GEMINI_25_PRO = "Gemini-2.5-Pro"
    GEMINI_31_PRO = "Gemini-3.1-Pro"

    # GPT 系列 (使用 m3a_agent) - 论文中有3个
    GPT_55 = "GPT-5.5"
    GPT_54 = "GPT-5.4"
    GPT_5 = "GPT-5"

    # Doubao-Seed 系列 (使用 seed_agent) - 论文中有3个
    DOUBAO_SEED_16 = "Doubao-Seed-1.6"
    DOUBAO_SEED_18 = "Doubao-Seed-1.8"
    DOUBAO_SEED_20 = "Doubao-Seed-2.0"

    # Qwen 系列 (使用 qwen3) - 论文中有2个
    QWEN_36_PLUS = "Qwen-3.6-Plus"
    QWEN_36_FLASH = "Qwen-3.6-Flash"

    # 其他开源模型 - 论文中有4个
    MOBILE_AGENT_V35 = "MobileAgent-v3.5"
    UI_TARS_15_7B = "UI-TARS-1.5-7B"
    AGENTCPM_GUI = "AgentCPM-GUI"
    V_DROID = "V-Droid"

    # ============ 代码中已有但论文未提及的模型（保留） ============

    # Doubao 其他系列
    DOUBAO_PRO_32K = "Doubao-pro-32k"
    DOUBAO_PRO_256K = "Doubao-pro-256k"

    # Seed 系列
    SEED15_VL = "Seed-1.5-VL"

    # UI-TARS 其他版本
    UI_TARS_15 = "UI-TARS-1.5"
    OPEN_SOURCE_UI_TRAS = "OpenSource-UI-TRAS"

    # GPT 其他版本
    GPT4O = "GPT-4o"

    # Gemini 其他版本
    GEMINI20_FLASH_EXP = "Gemini-2.0-Flash-exp"

    # Claude 其他版本
    CLAUDE35_SONNET = "Claude-3.5-Sonnet"
    CLAUDE45_SONNET = "Claude-4.5-Sonnet"

    # Qwen 其他版本
    QWEN25_VL_72B = "Qwen2.5-VL-72B"
    QWEN3_VL = "Qwen3-VL"

    # 通用 M3A Agent
    M3A_AGENT = "m3a_agent"


def create_agent(
    agent_name: BaselineEnum,
    device_id: str,
    screenshots_dir: str = "screenshots",
    app_package: str = "",
) -> BaseAgent:
    """
    创建 Agent 实例

    Args:
        agent_name: Baseline 模型类型（BaselineEnum）
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

    # Doubao 系列模型 (使用 seed_agent)
    if agent_name == BaselineEnum.DOUBAO_PRO_32K:
        from appsim.agents.seed_agent import SeedAgent

        api_key = os.getenv("DOUBAO_PRO_32K_API_KEY", api_key)
        base_url = os.getenv("DOUBAO_PRO_32K_API_BASE", base_url)
        model_name = os.getenv("DOUBAO_PRO_32K_MODEL_NAME", model_name)
        model_kwargs = {"temperature": 0.0, "top_p": 0.7}

        return SeedAgent(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == BaselineEnum.DOUBAO_PRO_256K:
        from appsim.agents.seed_agent import SeedAgent

        api_key = os.getenv("DOUBAO_PRO_256K_API_KEY", api_key)
        base_url = os.getenv("DOUBAO_PRO_256K_API_BASE", base_url)
        model_name = os.getenv("DOUBAO_PRO_256K_MODEL_NAME", model_name)
        model_kwargs = {"temperature": 0.0, "top_p": 0.7}

        return SeedAgent(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    # Seed 系列模型
    elif agent_name == BaselineEnum.SEED15_VL:
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

    # Doubao-Seed 系列模型 (使用 seed_agent)
    elif agent_name == BaselineEnum.DOUBAO_SEED_16:
        from appsim.agents.seed_agent import SeedAgent

        api_key = os.getenv("DOUBAO_SEED_16_API_KEY", api_key)
        base_url = os.getenv("DOUBAO_SEED_16_API_BASE", base_url)
        model_name = os.getenv("DOUBAO_SEED_16_MODEL_NAME", model_name)
        model_kwargs = {"temperature": 0.0, "top_p": 0.7}

        return SeedAgent(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == BaselineEnum.DOUBAO_SEED_18:
        from appsim.agents.seed_agent import SeedAgent

        api_key = os.getenv("DOUBAO_SEED_18_API_KEY", api_key)
        base_url = os.getenv("DOUBAO_SEED_18_API_BASE", base_url)
        model_name = os.getenv("DOUBAO_SEED_18_MODEL_NAME", model_name)
        model_kwargs = {"temperature": 0.0, "top_p": 0.7}

        return SeedAgent(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == BaselineEnum.DOUBAO_SEED_20:
        from appsim.agents.seed_agent import SeedAgent

        api_key = os.getenv("DOUBAO_SEED_20_API_KEY", api_key)
        base_url = os.getenv("DOUBAO_SEED_20_API_BASE", base_url)
        model_name = os.getenv("DOUBAO_SEED_20_MODEL_NAME", model_name)
        model_kwargs = {"temperature": 0.0, "top_p": 0.7}

        return SeedAgent(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == BaselineEnum.UI_TARS_15:
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

    elif agent_name == BaselineEnum.UI_TARS_15_7B:
        # 论文中的 UI-TARS-1.5-7B (使用 seed_agent)
        from appsim.agents.seed_agent import SeedAgent

        api_key = os.getenv("UI_TARS_15_7B_API_KEY", api_key)
        base_url = os.getenv("UI_TARS_15_7B_API_BASE", base_url)
        model_name = os.getenv("UI_TARS_15_7B_MODEL_NAME", model_name)
        model_kwargs = {"temperature": 0.0, "top_p": 0.7}

        return SeedAgent(
            api_key=api_key,
            base_url=base_url,
            model_name=model_name,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == BaselineEnum.M3A_AGENT:
        return _create_m3a_agent(api_key, base_url, model_name)

    # GPT 系列模型 (使用 m3a_agent)
    elif agent_name == BaselineEnum.GPT4O:
        api_key = os.getenv("GPT4O_API_KEY", api_key)
        base_url = os.getenv("GPT4O_API_BASE", base_url)
        model_name = os.getenv("GPT4O_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.GPT5:
        api_key = os.getenv("GPT5_API_KEY", api_key)
        base_url = os.getenv("GPT5_API_BASE", base_url)
        model_name = os.getenv("GPT5_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.GPT_54:
        api_key = os.getenv("GPT_54_API_KEY", api_key)
        base_url = os.getenv("GPT_54_API_BASE", base_url)
        model_name = os.getenv("GPT_54_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.GPT_55:
        api_key = os.getenv("GPT_55_API_KEY", api_key)
        base_url = os.getenv("GPT_55_API_BASE", base_url)
        model_name = os.getenv("GPT_55_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.GPT_5:
        api_key = os.getenv("GPT_5_API_KEY", api_key)
        base_url = os.getenv("GPT_5_API_BASE", base_url)
        model_name = os.getenv("GPT_5_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    # Gemini 系列模型 (使用 m3a_agent)
    elif agent_name == BaselineEnum.GEMINI20_FLASH_EXP:
        api_key = os.getenv("GEMINI20_FLASH_EXP_API_KEY", api_key)
        base_url = os.getenv("GEMINI20_FLASH_EXP_API_BASE", base_url)
        model_name = os.getenv("GEMINI20_FLASH_EXP_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.GEMINI25_PRO:
        api_key = os.getenv("GEMINI25_PRO_API_KEY", api_key)
        base_url = os.getenv("GEMINI25_PRO_API_BASE", base_url)
        model_name = os.getenv("GEMINI25_PRO_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.GEMINI_25_PRO:
        api_key = os.getenv("GEMINI_25_PRO_API_KEY", api_key)
        base_url = os.getenv("GEMINI_25_PRO_API_BASE", base_url)
        model_name = os.getenv("GEMINI_25_PRO_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.GEMINI_3_PRO:
        api_key = os.getenv("GEMINI_3_PRO_API_KEY", api_key)
        base_url = os.getenv("GEMINI_3_PRO_API_BASE", base_url)
        model_name = os.getenv("GEMINI_3_PRO_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.GEMINI_31_PRO:
        api_key = os.getenv("GEMINI_31_PRO_API_KEY", api_key)
        base_url = os.getenv("GEMINI_31_PRO_API_BASE", base_url)
        model_name = os.getenv("GEMINI_31_PRO_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    # Claude 系列模型 (使用 m3a_agent)
    elif agent_name == BaselineEnum.CLAUDE35_SONNET:
        api_key = os.getenv("CLAUDE35_SONNET_API_KEY", api_key)
        base_url = os.getenv("CLAUDE35_SONNET_API_BASE", base_url)
        model_name = os.getenv("CLAUDE35_SONNET_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.CLAUDE45_SONNET:
        api_key = os.getenv("CLAUDE45_SONNET_API_KEY", api_key)
        base_url = os.getenv("CLAUDE45_SONNET_API_BASE", base_url)
        model_name = os.getenv("CLAUDE45_SONNET_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.CLAUDE_OPUS_47:
        api_key = os.getenv("CLAUDE_OPUS_47_API_KEY", api_key)
        base_url = os.getenv("CLAUDE_OPUS_47_API_BASE", base_url)
        model_name = os.getenv("CLAUDE_OPUS_47_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.CLAUDE_SONNET_46:
        api_key = os.getenv("CLAUDE_SONNET_46_API_KEY", api_key)
        base_url = os.getenv("CLAUDE_SONNET_46_API_BASE", base_url)
        model_name = os.getenv("CLAUDE_SONNET_46_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.CLAUDE_HAIKU_45:
        api_key = os.getenv("CLAUDE_HAIKU_45_API_KEY", api_key)
        base_url = os.getenv("CLAUDE_HAIKU_45_API_BASE", base_url)
        model_name = os.getenv("CLAUDE_HAIKU_45_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    elif agent_name == BaselineEnum.CLAUDE_SONNET_45:
        api_key = os.getenv("CLAUDE_SONNET_45_API_KEY", api_key)
        base_url = os.getenv("CLAUDE_SONNET_45_API_BASE", base_url)
        model_name = os.getenv("CLAUDE_SONNET_45_MODEL_NAME", model_name)
        return _create_m3a_agent(api_key, base_url, model_name)

    # Qwen 系列模型 (使用 qwen3)
    elif agent_name == BaselineEnum.QWEN25_VL_72B:
        from appsim.agents.qwen3 import Qwen3Agent

        api_key = os.getenv("QWEN25_VL_72B_API_KEY", api_key)
        base_url = os.getenv("QWEN25_VL_72B_API_BASE", base_url)
        model_name = os.getenv("QWEN25_VL_72B_MODEL_NAME", model_name)
        model_kwargs = {}

        return Qwen3Agent(
            model_name=model_name,
            api_key=api_key,
            api_base=base_url,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == BaselineEnum.QWEN3_VL:
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

    # 论文中的 Qwen 系列模型
    elif agent_name == BaselineEnum.QWEN_36_PLUS:
        from appsim.agents.qwen3 import Qwen3Agent

        api_key = os.getenv("QWEN_36_PLUS_API_KEY", api_key)
        base_url = os.getenv("QWEN_36_PLUS_API_BASE", base_url)
        model_name = os.getenv("QWEN_36_PLUS_MODEL_NAME", model_name)
        model_kwargs = {}

        return Qwen3Agent(
            model_name=model_name,
            api_key=api_key,
            api_base=base_url,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == BaselineEnum.QWEN_36_FLASH:
        from appsim.agents.qwen3 import Qwen3Agent

        api_key = os.getenv("QWEN_36_FLASH_API_KEY", api_key)
        base_url = os.getenv("QWEN_36_FLASH_API_BASE", base_url)
        model_name = os.getenv("QWEN_36_FLASH_MODEL_NAME", model_name)
        model_kwargs = {}

        return Qwen3Agent(
            model_name=model_name,
            api_key=api_key,
            api_base=base_url,
            device_id=device_id,
            screenshots_dir=screenshots_dir,
            model_kwargs=model_kwargs,
        )

    elif agent_name == BaselineEnum.AGENTCPM_GUI:
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

    elif agent_name == BaselineEnum.OPEN_SOURCE_UI_TRAS:
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

    elif agent_name == BaselineEnum.MOBILE_AGENT_V35:
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

    elif agent_name == BaselineEnum.V_DROID:
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
