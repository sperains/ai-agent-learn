"""第 7 课的可执行契约：工具白名单与参数校验。"""

from pathlib import Path
import importlib.util
import sys

import pytest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_07_tool_registry_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def create_registry() -> main.ToolRegistry:
    registry = main.ToolRegistry()
    registry.register_add()
    return registry


def test_registered_add_tool_executes_with_valid_numeric_arguments() -> None:
    result = create_registry().execute(
        main.ToolCall(
            tool_name="add",
            arguments={"left": 2, "right": 3},
        )
    )

    assert result == 5


def test_unknown_tool_is_rejected_before_any_execution() -> None:
    with pytest.raises(ValueError, match="未注册的工具"):
        create_registry().execute(
            main.ToolCall(
                tool_name="delete_file",
                arguments={"path": "important.txt"},
            )
        )


def test_add_tool_rejects_missing_required_argument() -> None:
    with pytest.raises(ValueError, match="缺少参数 right"):
        create_registry().execute(
            main.ToolCall(
                tool_name="add",
                arguments={"left": 2},
            )
        )


def test_add_tool_rejects_non_numeric_argument() -> None:
    with pytest.raises(ValueError, match="参数 left 必须是数字"):
        create_registry().execute(
            main.ToolCall(
                tool_name="add",
                arguments={"left": "two", "right": 3},
            )
        )
