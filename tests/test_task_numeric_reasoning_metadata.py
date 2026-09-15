import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR / "src"))

from appsim.tasks import APP_TASKS_MAP
from appsim.tasks.base import NumericReasoningCategory

EXPECTED_APP_COUNTS = {
    "Amazon": 21,
    "Bilibili": 17,
    "Booking": 9,
    "EleMe": 21,
    "Gaode": 11,
    "Instagram": 2,
    "Music": 3,
    "MyJD": 27,
    "RedNote": 6,
    "Spotify": 3,
    "TencentMeeting": 10,
    "UberEats": 15,
    "Wechat": 5,
    "WhatsApp": 7,
    "YouTube": 13,
    "Zoom": 5,
    "ctrip_sim": 8,
}

EXPECTED_CATEGORY_COUNTS = {
    NumericReasoningCategory.COUNT: 65,
    NumericReasoningCategory.CALCULATE: 45,
    NumericReasoningCategory.COMPARE_SELECT: 75,
    NumericReasoningCategory.THRESHOLD_FILTER: 21,
}


class TaskNumericReasoningMetadataTest(unittest.TestCase):
    def test_numeric_reasoning_app_counts(self) -> None:
        actual = {
            app.value: sum(
                bool(task.numeric_reasoning_categories)
                for task in tasks.task_items
            )
            for app, tasks in APP_TASKS_MAP.items()
        }

        self.assertEqual(actual, EXPECTED_APP_COUNTS)

    def test_numeric_reasoning_category_counts(self) -> None:
        category_counts = Counter()
        multi_category_task_count = 0
        numeric_task_count = 0

        for tasks in APP_TASKS_MAP.values():
            for task in tasks.task_items:
                categories = task.numeric_reasoning_categories
                self.assertTrue(
                    all(
                        isinstance(category, NumericReasoningCategory)
                        for category in categories
                    )
                )
                if categories:
                    numeric_task_count += 1
                    category_counts.update(categories)
                    if len(categories) > 1:
                        multi_category_task_count += 1

        self.assertEqual(numeric_task_count, 183)
        self.assertEqual(multi_category_task_count, 21)
        self.assertEqual(category_counts, EXPECTED_CATEGORY_COUNTS)


if __name__ == "__main__":
    unittest.main()
