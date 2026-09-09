"""
Evaluation for Zoom task 16: Set availability to 'Busy' and display name to 'Liu Chenlong'.
"""

from __future__ import annotations

import logging
import os

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.zoom"
RUNTIME_PROFILE_STATE_FILE = "runtime_profile_state.json"

# Cache for runtime data
_RUNTIME_CACHE: dict[tuple[int, str, str | None, str | None], object] = {}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path."""
    if backup_dir:
        return backup_dir
    return os.path.join(os.getcwd(), "scripts", "zoom", f"task_{task_id:02d}")


def _read_runtime_json(task_id: int, filename: str, device_id: str | None, backup_dir: str | None):
    """Read runtime JSON from device or backup."""
    cache_key = (task_id, filename, device_id, backup_dir)
    if cache_key not in _RUNTIME_CACHE:
        resolved_backup_dir = _build_backup_dir(task_id, backup_dir)
        _RUNTIME_CACHE[cache_key] = read_json_from_device(
            device_id=device_id,
            package_name=PACKAGE_NAME,
            device_json_path=f"files/{filename}",
            backup_dir=resolved_backup_dir,
        )
    return _RUNTIME_CACHE[cache_key]


def _as_dict(value) -> dict:
    """Convert value to dict if possible."""
    return value if isinstance(value, dict) else {}


def _profile_state(task_id: int, device_id: str | None, backup_dir: str | None) -> dict:
    """Get the profile state."""
    return _as_dict(_read_runtime_json(task_id, RUNTIME_PROFILE_STATE_FILE, device_id, backup_dir))


def verify_change_display_name_to_liu_chenlong(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify that the profile display name is set to 'Liu Chenlong'.

    Task 16 logic from _shared.py lines 1164-1166.
    """
    task_id = 16

    profile = _profile_state(task_id, device_id, backup_dir)
    return str(profile.get("displayName", "")) == "Liu Chenlong"


if __name__ == "__main__":
    print(verify_change_display_name_to_liu_chenlong())
