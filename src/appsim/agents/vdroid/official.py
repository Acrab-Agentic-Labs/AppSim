"""加载 V-Droid 仓库中的官方提示词函数。"""

import importlib.util
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Callable


@dataclass(frozen=True)
class OfficialComponents:
    """AppSim 使用的最小官方接口。"""

    action_selection_prompt: Callable[[str, list[str], str, str], str]
    action_completion_prompt: Callable[[str, str, list[str], str], str]
    summarize_prompt: Callable[..., str]


def _load_module(module_name: str, module_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载 V-Droid 官方模块: {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=4)
def load_official_components(code_dir: str) -> OfficialComponents:
    """从 V-Droid 仓库加载官方 verifier 和动作补全提示词。"""

    resolved_code_dir = Path(code_dir).expanduser().resolve()
    prompt_path = resolved_code_dir / "prompt_template.py"
    if not prompt_path.is_file():
        raise FileNotFoundError(f"缺少 V-Droid 官方提示词文件: {prompt_path}")

    prompt_module = _load_module(
        "_appsim_vdroid_prompt_template",
        prompt_path,
    )
    return OfficialComponents(
        action_selection_prompt=prompt_module.action_selection_prompt_with_verifier,
        action_completion_prompt=prompt_module.action_completion_prompt,
        summarize_prompt=prompt_module.summarize_prompt,
    )
