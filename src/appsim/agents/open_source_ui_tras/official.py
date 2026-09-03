# -*- coding: utf-8 -*-
"""加载开源 UI-TARS 仓库中的官方提示词和动作解析器。"""

import importlib.util
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, Callable


@dataclass(frozen=True)
class OfficialComponents:
    """官方代码中供 AppSim 使用的最小接口。"""

    mobile_prompt: str
    parse_action: Callable[..., Any]
    add_box_token: Callable[[str], str]


def _load_module(module_name: str, module_path: Path) -> ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"无法加载官方模块: {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=4)
def load_official_components(code_dir: str) -> OfficialComponents:
    """从指定 UI-TARS codes 目录加载官方实现。"""

    resolved_code_dir = Path(code_dir).expanduser().resolve()
    package_dir = resolved_code_dir / "ui_tars"
    action_parser_path = package_dir / "action_parser.py"
    prompt_path = package_dir / "prompt.py"

    missing_files = [str(path) for path in (action_parser_path, prompt_path) if not path.is_file()]
    if missing_files:
        raise FileNotFoundError("缺少开源 UI-TARS 官方代码文件: " + ", ".join(missing_files))

    action_parser = _load_module(
        "_appsim_open_source_ui_tras_action_parser",
        action_parser_path,
    )
    prompt = _load_module(
        "_appsim_open_source_ui_tras_prompt",
        prompt_path,
    )

    return OfficialComponents(
        mobile_prompt=prompt.MOBILE_USE_DOUBAO,
        parse_action=action_parser.parse_action_to_structure_output,
        add_box_token=action_parser.add_box_token,
    )
