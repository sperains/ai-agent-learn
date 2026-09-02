"""第 4 课的可执行契约：模型文本的 JSON 解析与结构校验。"""

from pathlib import Path
import importlib.util
import sys

import pytest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_04_structured_output_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def test_parser_returns_a_validated_task_classification() -> None:
    result = main.parse_task_classification('{"urgent": true, "category": "bug"}')

    assert result == main.TaskClassification(urgent=True, category="bug")


def test_parser_rejects_text_that_is_not_valid_json() -> None:
    with pytest.raises(ValueError, match="模型响应不是有效 JSON"):
        main.parse_task_classification("紧急，类别是问题")


def test_parser_rejects_a_string_where_a_boolean_is_required() -> None:
    with pytest.raises(ValueError, match="urgent 必须是布尔值"):
        main.parse_task_classification('{"urgent": "yes", "category": "bug"}')


def test_parser_rejects_a_category_outside_the_allowed_values() -> None:
    with pytest.raises(ValueError, match="category 必须是 bug 或 question"):
        main.parse_task_classification('{"urgent": false, "category": "其他"}')
