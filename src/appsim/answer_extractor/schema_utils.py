# -*- coding:utf-8 -*-
import json
import re
from typing import Any, Dict, List, Tuple


def strip_markdown_fences(text: str) -> str:
    """移除常见的 markdown code fence。"""
    stripped = text.strip()
    if stripped.startswith("```"):
        stripped = re.sub(r"^```(?:json)?\s*", "", stripped)
        stripped = re.sub(r"\s*```$", "", stripped)
    return stripped.strip()


def extract_first_json_object(text: str) -> Any:
    """从文本中提取第一个 JSON 对象或数组。"""
    stripped = strip_markdown_fences(text)
    try:
        return json.loads(stripped)
    except Exception:
        pass

    decoder = json.JSONDecoder()
    for idx, char in enumerate(stripped):
        if char not in "{[":
            continue
        try:
            obj, _ = decoder.raw_decode(stripped[idx:])
            return obj
        except Exception:
            continue
    raise ValueError("无法从输出中解析 JSON")


def normalize_answer_by_schema(answer: Any, schema: Dict[str, Any]) -> Any:
    """按 schema 做最少量的通用归一化。"""
    if answer is None:
        # 方案 1：字段级 null 视为“未抽到答案”的合法值，保留给 verifier 决定是否接受。
        return None

    schema_type = schema.get("type")

    if schema_type == "object" and isinstance(answer, dict):
        properties = schema.get("properties", {})
        normalized = {}
        for key, value in answer.items():
            child_schema = properties.get(key, {})
            normalized[key] = normalize_answer_by_schema(value, child_schema)
        return normalized

    if schema_type == "array" and isinstance(answer, list):
        item_schema = schema.get("items", {})
        return [normalize_answer_by_schema(item, item_schema) for item in answer]

    if schema_type == "string":
        if answer is None:
            return None
        return str(answer).strip()

    if schema_type == "integer":
        if isinstance(answer, bool):
            raise ValueError("布尔值不能转换为 integer")
        if isinstance(answer, int):
            return answer
        if isinstance(answer, float) and answer.is_integer():
            return int(answer)
        if isinstance(answer, str):
            value = answer.strip()
            if re.fullmatch(r"[+-]?\d+", value):
                return int(value)
        raise ValueError(f"无法将值 {answer!r} 转换为 integer")

    if schema_type == "number":
        if isinstance(answer, bool):
            raise ValueError("布尔值不能转换为 number")
        if isinstance(answer, (int, float)):
            return answer
        if isinstance(answer, str):
            value = answer.strip()
            if re.fullmatch(r"[+-]?\d+(?:\.\d+)?", value):
                return float(value) if "." in value else int(value)
        raise ValueError(f"无法将值 {answer!r} 转换为 number")

    if schema_type == "boolean":
        if isinstance(answer, bool):
            return answer
        if isinstance(answer, str):
            value = answer.strip().lower()
            if value in {"true", "yes"}:
                return True
            if value in {"false", "no"}:
                return False
        raise ValueError(f"无法将值 {answer!r} 转换为 boolean")

    return answer


def validate_answer_by_schema(answer: Any, schema: Dict[str, Any], path: str = "$") -> List[str]:
    """使用极简 JSON Schema 子集校验答案。"""
    errors: List[str] = []
    schema_type = schema.get("type")

    if answer is None and path != "$":
        return errors

    if schema_type == "object":
        if not isinstance(answer, dict):
            return [f"{path} 不是 object"]

        properties = schema.get("properties", {})
        required = schema.get("required", [])
        additional_allowed = schema.get("additionalProperties", True)

        for field in required:
            if field not in answer:
                errors.append(f"{path}.{field} 缺失")

        for key, value in answer.items():
            if key in properties:
                errors.extend(validate_answer_by_schema(value, properties[key], f"{path}.{key}"))
            elif additional_allowed is False:
                errors.append(f"{path}.{key} 不允许出现")
        return errors

    if schema_type == "array":
        if not isinstance(answer, list):
            return [f"{path} 不是 array"]
        min_items = schema.get("minItems")
        max_items = schema.get("maxItems")
        if min_items is not None and len(answer) < min_items:
            errors.append(f"{path} 元素个数小于 {min_items}")
        if max_items is not None and len(answer) > max_items:
            errors.append(f"{path} 元素个数大于 {max_items}")
        if schema.get("uniqueItems"):
            normalized = [json.dumps(item, ensure_ascii=False, sort_keys=True) for item in answer]
            if len(normalized) != len(set(normalized)):
                errors.append(f"{path} 存在重复元素")
        item_schema = schema.get("items")
        if item_schema:
            for idx, item in enumerate(answer):
                errors.extend(validate_answer_by_schema(item, item_schema, f"{path}[{idx}]"))
        return errors

    if schema_type == "string":
        if not isinstance(answer, str):
            return [f"{path} 不是 string"]
        min_length = schema.get("minLength")
        if min_length is not None and len(answer) < min_length:
            errors.append(f"{path} 长度小于 {min_length}")
        pattern = schema.get("pattern")
        if pattern and re.fullmatch(pattern, answer) is None:
            errors.append(f"{path} 不匹配 pattern {pattern}")
        enum = schema.get("enum")
        if enum is not None and answer not in enum:
            errors.append(f"{path} 不在 enum 中")
        const = schema.get("const")
        if const is not None and answer != const:
            errors.append(f"{path} 不等于 const")
        return errors

    if schema_type == "integer":
        if isinstance(answer, bool) or not isinstance(answer, int):
            return [f"{path} 不是 integer"]
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        enum = schema.get("enum")
        const = schema.get("const")
        if minimum is not None and answer < minimum:
            errors.append(f"{path} 小于 minimum {minimum}")
        if maximum is not None and answer > maximum:
            errors.append(f"{path} 大于 maximum {maximum}")
        if enum is not None and answer not in enum:
            errors.append(f"{path} 不在 enum 中")
        if const is not None and answer != const:
            errors.append(f"{path} 不等于 const")
        return errors

    if schema_type == "number":
        if isinstance(answer, bool) or not isinstance(answer, (int, float)):
            return [f"{path} 不是 number"]
        minimum = schema.get("minimum")
        maximum = schema.get("maximum")
        enum = schema.get("enum")
        const = schema.get("const")
        if minimum is not None and answer < minimum:
            errors.append(f"{path} 小于 minimum {minimum}")
        if maximum is not None and answer > maximum:
            errors.append(f"{path} 大于 maximum {maximum}")
        if enum is not None and answer not in enum:
            errors.append(f"{path} 不在 enum 中")
        if const is not None and answer != const:
            errors.append(f"{path} 不等于 const")
        return errors

    if schema_type == "boolean":
        if not isinstance(answer, bool):
            return [f"{path} 不是 boolean"]
        return errors

    enum = schema.get("enum")
    if enum is not None and answer not in enum:
        errors.append(f"{path} 不在 enum 中")
    const = schema.get("const")
    if const is not None and answer != const:
        errors.append(f"{path} 不等于 const")
    return errors


def schema_to_prompt(schema: Dict[str, Any]) -> str:
    """将 schema 序列化为更适合放入 prompt 的字符串。"""
    return json.dumps(schema, ensure_ascii=False, indent=2)


def validate_and_normalize(answer: Any, schema: Dict[str, Any]) -> Tuple[Any, List[str]]:
    """先做最少量归一化，再用 schema 校验。"""
    normalized = normalize_answer_by_schema(answer, schema)
    errors = validate_answer_by_schema(normalized, schema)
    return normalized, errors
