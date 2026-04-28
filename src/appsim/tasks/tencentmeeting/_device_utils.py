from __future__ import annotations

import html
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import xml.etree.ElementTree as ET
from typing import Any, Iterable


def default_backup_dir(name: str) -> str:
    return os.path.join(os.getcwd(), "scripts_backup", name)


def _ensure_backup_dir(backup_dir: str | None) -> Path | None:
    if not backup_dir:
        return None
    path = Path(backup_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_adb_executable() -> str:
    return os.environ.get("ADBUTILS_ADB_PATH") or "adb"


def _adb_command(device_id: str | None, *args: str) -> list[str]:
    command = [get_adb_executable()]
    if device_id:
        command.extend(["-s", str(device_id)])
    command.extend(str(arg) for arg in args)
    return command


def run_adb(device_id: str | None, *args: str, timeout: float = 15.0) -> subprocess.CompletedProcess[str] | None:
    try:
        return subprocess.run(
            _adb_command(device_id, *args),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout,
        )
    except FileNotFoundError as exc:
        logging.error("adb executable was not found: %s", exc)
    except subprocess.TimeoutExpired as exc:
        logging.error("adb command timed out: %s", exc)
    except Exception as exc:
        logging.error("adb command failed unexpectedly: %s", exc)
    return None


def read_json_from_device(
    device_id: str | None,
    package_name: str,
    device_json_path: str,
    backup_dir: str | None,
    required: bool = True,
) -> Any | None:
    """Read a JSON file from the app sandbox and store a local backup."""

    backup_path = _ensure_backup_dir(backup_dir)
    local_file_path = None
    if backup_path is not None:
        local_file_path = backup_path / Path(device_json_path).name

    ls_result = run_adb(device_id, "exec-out", "run-as", package_name, "ls", device_json_path)
    if ls_result is None:
        return None

    ls_output = f"{ls_result.stdout}\n{ls_result.stderr}"
    if ls_result.returncode != 0 or "No such file or directory" in ls_output:
        if required:
            logging.error("Device file is not available: %s", device_json_path)
        else:
            logging.info("Optional device file is not available: %s", device_json_path)
        return None

    cat_result = run_adb(device_id, "exec-out", "run-as", package_name, "cat", device_json_path, timeout=20.0)
    if cat_result is None:
        return None
    if cat_result.returncode != 0:
        logging.error("Unable to read device file %s: %s", device_json_path, cat_result.stderr.strip())
        return None

    text = cat_result.stdout.lstrip("\ufeff")
    if local_file_path is not None:
        try:
            local_file_path.write_text(text, encoding="utf-8")
        except Exception as exc:
            logging.warning("Unable to write backup %s: %s", local_file_path, exc)

    try:
        return json.loads(text, strict=False)
    except json.JSONDecodeError as exc:
        logging.error("Unable to parse JSON from %s: %s", device_json_path, exc)
    except Exception as exc:
        logging.error("Unexpected JSON read error for %s: %s", device_json_path, exc)
    return None


def list_records(data: Any) -> list[dict[str, Any]]:
    if not isinstance(data, list):
        return []
    return [item for item in data if isinstance(item, dict)]


def dump_current_ui(device_id: str | None, backup_dir: str | None = None) -> str:
    """Return the current UIAutomator XML dump, or an empty string on failure."""

    backup_path = _ensure_backup_dir(backup_dir)
    remote_path = "/sdcard/appsim_window_dump.xml"
    dump_result = run_adb(device_id, "shell", "uiautomator", "dump", remote_path, timeout=20.0)
    if dump_result is None:
        return ""
    if dump_result.returncode != 0:
        logging.error("uiautomator dump failed: %s", (dump_result.stderr or dump_result.stdout).strip())
        return ""

    cat_result = run_adb(device_id, "exec-out", "cat", remote_path, timeout=20.0)
    if cat_result is None or cat_result.returncode != 0 or not cat_result.stdout:
        cat_result = run_adb(device_id, "shell", "cat", remote_path, timeout=20.0)

    if cat_result is None or cat_result.returncode != 0:
        logging.error("Unable to read UI dump from device")
        return ""

    raw_xml = cat_result.stdout or ""
    if backup_path is not None:
        try:
            (backup_path / "window_dump.xml").write_text(raw_xml, encoding="utf-8")
        except Exception as exc:
            logging.warning("Unable to write UI dump backup: %s", exc)
    return raw_xml


def _attribute_values_from_xml(raw_xml: str) -> list[str]:
    values: list[str] = []
    if not raw_xml:
        return values

    try:
        root = ET.fromstring(raw_xml)
        for node in root.iter():
            for attr in ("text", "content-desc"):
                value = node.attrib.get(attr)
                if value:
                    values.append(value)
    except ET.ParseError:
        for attr in ("text", "content-desc"):
            values.extend(re.findall(rf'{attr}="([^"]*)"', raw_xml))
    return values


def extract_ui_text(raw_xml: str) -> str:
    values = [html.unescape(value) for value in _attribute_values_from_xml(raw_xml)]
    values.append(raw_xml)
    return normalize_text(" ".join(values))


def current_ui_text(device_id: str | None, backup_dir: str | None = None) -> str:
    return extract_ui_text(dump_current_ui(device_id, backup_dir))


def normalize_text(value: Any) -> str:
    text = html.unescape(str(value or ""))
    text = text.replace("\u00a0", " ").replace("\r", " ").replace("\n", " ").replace("\t", " ")
    return re.sub(r"\s+", " ", text).strip()


def contains_text(haystack: Any, needles: Iterable[Any]) -> bool:
    normalized_haystack = normalize_text(haystack).casefold()
    for needle in needles:
        if needle is None:
            continue
        normalized_needle = normalize_text(needle).casefold()
        if normalized_needle and normalized_needle in normalized_haystack:
            return True
    return False


def compact_digits(value: Any) -> str:
    return re.sub(r"\D+", "", str(value or ""))


def _decode_service_call_utf16(output: str) -> str:
    """Decode UTF-16 strings embedded in Android service-call hex dumps."""

    words: list[str] = []
    for line in output.splitlines():
        if not re.search(r"0x[0-9a-fA-F]+:", line):
            continue
        payload = line.split(":", 1)[1].split("'", 1)[0]
        words.extend(re.findall(r"\b[0-9a-fA-F]{8}\b", payload))

    decoded: list[str] = []
    for high_first in (True, False):
        chars: list[str] = []
        for word in words:
            halves = (word[:4], word[4:]) if high_first else (word[4:], word[:4])
            for half in halves:
                code_point = int(half, 16)
                if code_point == 0:
                    continue
                if 0xD800 <= code_point <= 0xDFFF:
                    continue
                if code_point in (9, 10, 13) or 32 <= code_point <= 0x10FFFF:
                    chars.append(chr(code_point))
                else:
                    chars.append(" ")
        text = normalize_text("".join(chars))
        if text:
            decoded.append(text)
    return "\n".join(dict.fromkeys(decoded))


def read_clipboard_text(device_id: str | None, backup_dir: str | None = None) -> str:
    """Best-effort clipboard read for emulator/manual verification checks."""

    commands: list[tuple[str, tuple[str, ...]]] = [
        ("cmd clipboard get", ("shell", "cmd", "clipboard", "get")),
        ("cmd clipboard get --user 0", ("shell", "cmd", "clipboard", "get", "--user", "0")),
        ("cmd clipboard --user 0 get", ("shell", "cmd", "clipboard", "--user", "0", "get")),
        ("dumpsys clipboard", ("shell", "dumpsys", "clipboard")),
        ("service call clipboard 1", ("shell", "service", "call", "clipboard", "1")),
        ("service call clipboard 2", ("shell", "service", "call", "clipboard", "2")),
    ]
    chunks: list[str] = []
    for label, args in commands:
        result = run_adb(device_id, *args, timeout=10.0)
        if result is None:
            continue
        output = f"{result.stdout}\n{result.stderr}".strip()
        if output:
            chunks.append(f"--- {label} ---\n{output}")
            if label.startswith("service call clipboard"):
                decoded = _decode_service_call_utf16(output)
                if decoded:
                    chunks.append(f"--- {label} decoded utf16 ---\n{decoded}")

    clipboard_text = "\n".join(chunks)
    backup_path = _ensure_backup_dir(backup_dir)
    if backup_path is not None:
        try:
            (backup_path / "clipboard.txt").write_text(clipboard_text, encoding="utf-8")
        except Exception as exc:
            logging.warning("Unable to write clipboard backup: %s", exc)
    return clipboard_text
