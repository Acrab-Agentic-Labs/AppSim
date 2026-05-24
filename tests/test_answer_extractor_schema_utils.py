import importlib.util
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).resolve().parents[1] / "src" / "appsim" / "answer_extractor" / "schema_utils.py"
SPEC = importlib.util.spec_from_file_location("schema_utils", MODULE_PATH)
schema_utils = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(schema_utils)


class SchemaUtilsNullHandlingTest(unittest.TestCase):
    def test_required_integer_field_accepts_null_value(self) -> None:
        schema = {
            "type": "object",
            "properties": {"friend_count": {"type": "integer", "minimum": 0}},
            "required": ["friend_count"],
            "additionalProperties": False,
        }

        normalized, errors = schema_utils.validate_and_normalize({"friend_count": None}, schema)

        self.assertEqual(normalized, {"friend_count": None})
        self.assertEqual(errors, [])

    def test_required_nested_object_accepts_null_value(self) -> None:
        schema = {
            "type": "object",
            "properties": {
                "meeting_info": {
                    "type": "object",
                    "properties": {"location": {"type": "string"}},
                    "required": ["location"],
                    "additionalProperties": False,
                }
            },
            "required": ["meeting_info"],
            "additionalProperties": False,
        }

        normalized, errors = schema_utils.validate_and_normalize({"meeting_info": None}, schema)

        self.assertEqual(normalized, {"meeting_info": None})
        self.assertEqual(errors, [])

    def test_missing_required_key_still_fails(self) -> None:
        schema = {
            "type": "object",
            "properties": {"person_name": {"type": "string", "minLength": 1}},
            "required": ["person_name"],
            "additionalProperties": False,
        }

        normalized, errors = schema_utils.validate_and_normalize({}, schema)

        self.assertEqual(normalized, {})
        self.assertEqual(errors, ["$.person_name 缺失"])

    def test_root_object_must_still_be_object(self) -> None:
        schema = {
            "type": "object",
            "properties": {"person_name": {"type": "string"}},
            "required": ["person_name"],
            "additionalProperties": False,
        }

        normalized, errors = schema_utils.validate_and_normalize(None, schema)

        self.assertIsNone(normalized)
        self.assertEqual(errors, ["$ 不是 object"])


if __name__ == "__main__":
    unittest.main()
