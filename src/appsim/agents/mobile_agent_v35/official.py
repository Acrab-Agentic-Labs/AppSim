"""加载仓库内的 Mobile-Agent-v3.5 官方实现。"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Optional, Type

CODE_DIR_ENV = "MOBILE_AGENT_V35_CODE_DIR"
_OFFICIAL_RELATIVE_DIR = Path("ModelRepos/MobileAgent/Mobile-Agent-v3.5/android_world_v3.5")
_REQUIRED_FILES = (
    Path("run_ma35.py"),
    Path("android_world/__init__.py"),
    Path("android_world/agents/mobile_agent_v3.py"),
    Path("android_world/agents/mobile_agent_v3_agent.py"),
    Path("android_world/agents/infer_ma3.py"),
    Path("android_world/agents/new_json_action.py"),
    Path("android_world/env/interface.py"),
)


class OfficialMobileAgentImportError(RuntimeError):
    """官方 Mobile-Agent-v3.5 无法定位或导入。"""


@dataclass(frozen=True)
class OfficialBindings:
    """AppSim 需要使用的官方类、函数和模块。"""

    code_dir: Path
    MobileAgentV3_M3A: Type[Any]
    GUIOwlWrapper: Type[Any]
    MultimodalLlmWrapper: Type[Any]
    InfoPool: Type[Any]
    Manager: Type[Any]
    Executor: Type[Any]
    Notetaker: Type[Any]
    ActionReflector: Type[Any]
    JSONAction: Type[Any]
    AsyncEnv: Type[Any]
    State: Type[Any]
    AgentInteractionResult: Type[Any]
    convert_fc_action_to_json_action: Callable[..., Any]
    mobile_agent_v3: ModuleType
    infer_ma3: ModuleType
    mobile_agent_v3_agent: ModuleType
    new_json_action: ModuleType
    interface: ModuleType
    base_agent: ModuleType


def _discover_default_code_dir() -> Path:
    configured = os.getenv(CODE_DIR_ENV)
    if configured:
        return Path(configured).expanduser().resolve()

    current_file = Path(__file__).resolve()
    for parent in current_file.parents:
        candidate = parent / _OFFICIAL_RELATIVE_DIR
        if candidate.is_dir():
            return candidate.resolve()

    raise OfficialMobileAgentImportError(
        "找不到 Mobile-Agent-v3.5 官方源码目录。"
        f"请设置 {CODE_DIR_ENV}，其值应指向包含 run_ma35.py 和 android_world/ 的目录。"
    )


def resolve_official_code_dir(
    code_dir: Optional[os.PathLike[str] | str] = None,
) -> Path:
    """解析并校验官方源码目录。"""

    resolved = Path(code_dir).expanduser().resolve() if code_dir is not None else _discover_default_code_dir()
    if not resolved.is_dir():
        raise OfficialMobileAgentImportError(f"Mobile-Agent-v3.5 code_dir 不存在或不是目录: {resolved}")

    missing = [str(path) for path in _REQUIRED_FILES if not (resolved / path).is_file()]
    if missing:
        missing_text = ", ".join(missing)
        raise OfficialMobileAgentImportError(
            f"code_dir 不是预期的 Mobile-Agent-v3.5 android_world_v3.5 目录: {resolved}；缺少文件: {missing_text}"
        )
    return resolved


def _is_inside(path: Path, directory: Path) -> bool:
    try:
        path.relative_to(directory)
        return True
    except ValueError:
        return False


def _loaded_android_world_origin() -> Optional[Path]:
    package = sys.modules.get("android_world")
    if package is None:
        return None

    package_file = getattr(package, "__file__", None)
    if package_file:
        return Path(package_file).resolve().parent

    package_paths = getattr(package, "__path__", None)
    if package_paths:
        first_path = next(iter(package_paths), None)
        if first_path:
            return Path(first_path).resolve()
    return None


def _put_code_dir_first(code_dir: Path) -> None:
    code_dir_text = str(code_dir)
    retained = []
    for entry in sys.path:
        try:
            is_same = Path(entry).expanduser().resolve() == code_dir
        except (OSError, RuntimeError):
            is_same = False
        if not is_same:
            retained.append(entry)
    sys.path[:] = [code_dir_text, *retained]


def _validate_module_origin(
    module: ModuleType,
    code_dir: Path,
) -> None:
    module_file = getattr(module, "__file__", None)
    if not module_file:
        raise OfficialMobileAgentImportError(f"无法确认官方模块来源: {module.__name__}")

    origin = Path(module_file).resolve()
    if not _is_inside(origin, code_dir):
        raise OfficialMobileAgentImportError(f"模块 {module.__name__} 来自其他目录: {origin}；预期目录: {code_dir}")


def _require_attr(module: ModuleType, name: str) -> Any:
    value = getattr(module, name, None)
    if value is None:
        raise OfficialMobileAgentImportError(
            f"官方模块 {module.__name__} 缺少对象 {name}，请确认源码版本为 Mobile-Agent-v3.5。"
        )
    return value


@lru_cache(maxsize=None)
def _load_official_bindings(code_dir_text: str) -> OfficialBindings:
    code_dir = Path(code_dir_text).resolve()
    expected_package_dir = code_dir / "android_world"
    loaded_origin = _loaded_android_world_origin()
    if loaded_origin is not None and not _is_inside(loaded_origin, expected_package_dir):
        raise OfficialMobileAgentImportError(
            "当前进程已加载其他 android_world 包: "
            f"{loaded_origin}；预期官方包: {expected_package_dir}。请在新进程中运行评测。"
        )

    _put_code_dir_first(code_dir)

    try:
        # 这些对象必须直接来自官方源码，适配层不得复制提示词或解析器。
        from android_world.agents import base_agent, infer_ma3, mobile_agent_v3, mobile_agent_v3_agent, new_json_action
        from android_world.env import interface
    except Exception as exc:
        requirements = code_dir / "requirements.txt"
        raise OfficialMobileAgentImportError(
            f"导入 Mobile-Agent-v3.5 官方模块失败。code_dir={code_dir}；请安装 {requirements} 中的依赖。原始错误: {exc}"
        ) from exc

    modules = (
        base_agent,
        infer_ma3,
        mobile_agent_v3,
        mobile_agent_v3_agent,
        new_json_action,
        interface,
    )
    for module in modules:
        _validate_module_origin(module, code_dir)

    return OfficialBindings(
        code_dir=code_dir,
        MobileAgentV3_M3A=_require_attr(mobile_agent_v3, "MobileAgentV3_M3A"),
        GUIOwlWrapper=_require_attr(infer_ma3, "GUIOwlWrapper"),
        MultimodalLlmWrapper=_require_attr(infer_ma3, "MultimodalLlmWrapper"),
        InfoPool=_require_attr(mobile_agent_v3_agent, "InfoPool"),
        Manager=_require_attr(mobile_agent_v3_agent, "Manager"),
        Executor=_require_attr(mobile_agent_v3_agent, "Executor"),
        Notetaker=_require_attr(mobile_agent_v3_agent, "Notetaker"),
        ActionReflector=_require_attr(mobile_agent_v3_agent, "ActionReflector"),
        JSONAction=_require_attr(new_json_action, "JSONAction"),
        AsyncEnv=_require_attr(interface, "AsyncEnv"),
        State=_require_attr(interface, "State"),
        AgentInteractionResult=_require_attr(base_agent, "AgentInteractionResult"),
        convert_fc_action_to_json_action=_require_attr(mobile_agent_v3, "convert_fc_action_to_json_action"),
        mobile_agent_v3=mobile_agent_v3,
        infer_ma3=infer_ma3,
        mobile_agent_v3_agent=mobile_agent_v3_agent,
        new_json_action=new_json_action,
        interface=interface,
        base_agent=base_agent,
    )


def load_official_bindings(
    code_dir: Optional[os.PathLike[str] | str] = None,
) -> OfficialBindings:
    """返回缓存的 Mobile-Agent-v3.5 官方对象集合。"""

    if sys.version_info < (3, 11):
        raise OfficialMobileAgentImportError("Mobile-Agent-v3.5 官方 AndroidWorld 代码要求 Python 3.11 或更高版本。")
    resolved = resolve_official_code_dir(code_dir)
    return _load_official_bindings(str(resolved))


def clear_official_bindings_cache() -> None:
    """清空导入结果缓存，主要供隔离测试使用。"""

    _load_official_bindings.cache_clear()


__all__ = [
    "CODE_DIR_ENV",
    "OfficialBindings",
    "OfficialMobileAgentImportError",
    "clear_official_bindings_cache",
    "load_official_bindings",
    "resolve_official_code_dir",
]
