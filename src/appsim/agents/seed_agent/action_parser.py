import json
import re
from typing import Any, Dict, List


class ActionParser:
    """AI动作输出解析器 - 支持灵活的参数顺序和别名"""

    def __init__(self):
        # 参数别名映射
        self.param_aliases = {
            "start_box": "point",  # start_box是point的别名
            "start_point": "start_point",
            "end_point": "end_point",
        }

    def parse_ai_response(self, ai_response: str) -> List[Dict[str, Any]]:
        """
        解析AI响应中的所有动作

        Args:
            ai_response: AI的完整响应文本

        Returns:
            List[Dict]: 解析出的动作列表
        """
        actions = []

        # 尝试解析JSON格式的动作
        json_matches = re.findall(r"```json\s*(.*?)\s*```", ai_response, re.DOTALL)
        for json_str in json_matches:
            self._parse_json_format(json_str.strip(), actions)

        # 解析函数调用格式的动作
        self._parse_function_call_format(ai_response, actions)

        return actions

    def _parse_json_format(self, json_str: str, actions: List[Dict[str, Any]]):
        """解析JSON格式的动作"""
        try:
            parsed = json.loads(json_str)
            if isinstance(parsed, list):
                actions.extend(parsed)
            else:
                actions.append(parsed)
        except json.JSONDecodeError:
            pass

    def _parse_function_call_format(self, text: str, actions: List[Dict[str, Any]]):
        """解析函数调用格式的动作 - 支持灵活参数顺序"""

        # 简单动作的正则（无参数或单参数）
        simple_patterns = {
            "click": r"click\(point='([^']+)'\)",
            "long_press": r"long_press\(point='([^']+)'\)",
            "type": r"type\(content='([^']+)'\)",
            "open_app": r"open_app\(app_name='([^']+)'\)",
            "press_home": r"press_home\(\)",
            "press_back": r"press_back\(\)",
            "finished": r"finished\(content='(.+?)'\)",
        }

        # 处理简单动作
        for action_type, pattern in simple_patterns.items():
            matches = re.findall(pattern, text)
            for match in matches:
                if action_type in ["click", "long_press"]:
                    actions.append({"action": action_type, "point": match})
                elif action_type == "type":
                    actions.append({"action": action_type, "content": match})
                elif action_type == "open_app":
                    actions.append({"action": action_type, "app_name": match})
                elif action_type in ["press_home", "press_back"]:
                    actions.append({"action": action_type})
                elif action_type == "finished":
                    actions.append({"action": action_type, "content": match})

        # 处理复杂动作（多参数，支持灵活顺序）
        self._parse_scroll_flexible(text, actions)
        self._parse_drag_flexible(text, actions)

    def _parse_scroll_flexible(self, text: str, actions: List[Dict[str, Any]]):
        """灵活解析scroll动作"""
        scroll_matches = re.findall(r"scroll\(([^)]+)\)", text)
        for params_str in scroll_matches:
            params = self._parse_params_flexible(params_str)

            # 检查必需参数
            point = params.get("point")
            direction = params.get("direction")

            if point and direction:
                actions.append({"action": "scroll", "point": point, "direction": direction})

    def _parse_drag_flexible(self, text: str, actions: List[Dict[str, Any]]):
        """灵活解析drag动作"""
        drag_matches = re.findall(r"drag\(([^)]+)\)", text)
        for params_str in drag_matches:
            params = self._parse_params_flexible(params_str)

            # 检查必需参数
            start_point = params.get("start_point")
            end_point = params.get("end_point")

            if start_point and end_point:
                actions.append({"action": "drag", "start_point": start_point, "end_point": end_point})

    def _parse_params_flexible(self, params_str: str) -> Dict[str, str]:
        """
        灵活解析参数字符串，支持参数乱序和别名

        Args:
            params_str: 参数字符串，如 "direction='up', point='<point>500 489</point>'"

        Returns:
            Dict: 解析后的参数字典
        """
        result = {}

        # 匹配所有 key='value' 格式的参数
        for param_match in re.finditer(r"(\w+)='([^']+)'", params_str):
            key = param_match.group(1)
            value = param_match.group(2)

            # 处理别名
            normalized_key = self.param_aliases.get(key, key)
            result[normalized_key] = value

        return result

    def validate_action(self, action: Dict[str, Any]) -> bool:
        """
        验证动作是否有效

        Args:
            action: 动作字典

        Returns:
            bool: 是否有效
        """
        action_type = action.get("action")

        if not action_type:
            return False

        # 验证必需参数
        required_params = {
            "click": ["point"],
            "long_press": ["point"],
            "type": ["content"],
            "scroll": ["point", "direction"],
            "open_app": ["app_name"],
            "drag": ["start_point", "end_point"],
            "press_home": [],
            "press_back": [],
            "finished": ["content"],
        }

        if action_type not in required_params:
            return False

        # 检查必需参数是否存在
        for param in required_params[action_type]:
            if param not in action or not action[param]:
                return False

        return True
