from __future__ import annotations

import re

from appsim.utils import read_json_from_device

# Constants
PACKAGE_NAME = "com.example.booking"
RUNTIME_HOTEL_REVIEW_SIGNALS_FILE_NAME = "runtime_hotel_review_signals.json"
RESULT_SKIP_KEYS = {"point", "path", "screenshot_path", "image"}


def _build_backup_dir(task_id: int, backup_dir: str | None) -> str:
    """Build the backup directory path for a task."""
    if backup_dir:
        return backup_dir
    import os
    return os.path.join(os.getcwd(), "scripts", "booking", f"task_{task_id:02d}")


def _read_runtime_json(task_id: int, filename: str, device_id: str | None, backup_dir: str | None):
    """Read JSON from device or backup directory."""
    return read_json_from_device(
        device_id=device_id,
        package_name=PACKAGE_NAME,
        device_json_path=f"files/{filename}",
        backup_dir=_build_backup_dir(task_id, backup_dir),
    )


def _as_list(value) -> list:
    """Ensure value is a list."""
    return value if isinstance(value, list) else []


def _hotel_review_signals(task_id: int, device_id: str | None, backup_dir: str | None) -> list[dict]:
    """Get hotel review signals from runtime data."""
    payload = _read_runtime_json(task_id, RUNTIME_HOTEL_REVIEW_SIGNALS_FILE_NAME, device_id, backup_dir)
    return [item for item in _as_list(payload) if isinstance(item, dict)]


def _find_latest(records: list[dict], predicate) -> dict | None:
    """Find the latest record matching the predicate."""
    for item in reversed(records):
        if predicate(item):
            return item
    return None


def _int_value(value, default: int = 0) -> int:
    """Convert value to int, returning default on error."""
    try:
        return int(value)
    except Exception:
        return default


def _append_named_strings(source: dict, keys: tuple[str, ...], chunks: list[str]) -> None:
    """Append named string values from source dict to chunks."""
    for key in keys:
        value = source.get(key)
        if isinstance(value, str):
            text = value.strip()
            if text:
                chunks.append(text)


def _collect_all_strings(value, chunks: list[str]) -> None:
    """Recursively collect all string values from nested structures."""
    if isinstance(value, str):
        text = value.strip()
        if text:
            chunks.append(text)
        return
    if isinstance(value, dict):
        for key, item in value.items():
            if key in RESULT_SKIP_KEYS:
                continue
            _collect_all_strings(item, chunks)
        return
    if isinstance(value, list):
        for item in value:
            _collect_all_strings(item, chunks)


def _extract_result_text(result) -> str:
    """Extract text from specific result fields."""
    if not isinstance(result, dict):
        return ""
    chunks: list[str] = []
    _append_named_strings(result, ("final_answer", "answer", "content", "message", "final_message", "summary"), chunks)
    for action in _as_list(result.get("executed_actions")):
        if isinstance(action, dict):
            _append_named_strings(action, ("content", "message", "text", "thought", "reason", "observation", "status", "description"), chunks)
    return "\n".join(chunks)


def _extract_result_broad_text(result) -> str:
    """Extract all text from result structure."""
    if not isinstance(result, dict):
        return ""
    chunks: list[str] = []
    _collect_all_strings(result, chunks)
    return "\n".join(chunks)


def _normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    lowered = text.replace("-", " ").replace("_", " ").lower()
    return re.sub(r"\s+", " ", lowered).strip()


def _result_contains_any_group(result, groups: list[list[str]], *, broad: bool = False) -> bool:
    """Check if result contains any of the specified keyword groups."""
    text = _extract_result_broad_text(result) if broad else _extract_result_text(result)
    normalized = _normalize_text(text)
    if not normalized:
        return False
    return any(all(_normalize_text(token) in normalized for token in group) for group in groups)


def verify_submit_five_star_review_for_last_stay(
    result=None,
    device_id=None,
    backup_dir=None,
    **kwargs,
) -> bool:
    """
    Verify task 4: Submit a five-star review for the last stay.

    Checks if:
    1. A hotel review signal exists for orderId="ord001" and hotelId="htl001" with rating=5
    2. OR the result contains keywords indicating a five-star review was submitted

    Args:
        result: The task execution result
        device_id: The device ID to read data from
        backup_dir: The backup directory path
        **kwargs: Additional arguments (ignored)

    Returns:
        bool: True if verification passes, False otherwise
    """
    task_id = 4

    # Check JSON signals for a 5-star review on ord001/htl001
    review = _find_latest(
        _hotel_review_signals(task_id, device_id, backup_dir),
        lambda signal: str(signal.get("orderId", "")) == "ord001" and str(signal.get("hotelId", "")) == "htl001"
    )
    json_ok = bool(review and _int_value(review.get("rating")) == 5)

    # Fallback: check result text for keywords
    fallback_ok = _result_contains_any_group(result, [["five", "star", "review"], ["5", "star", "review"]], broad=True)

    return json_ok or fallback_ok


if __name__ == "__main__":
    print(verify_submit_five_star_review_for_last_stay())

