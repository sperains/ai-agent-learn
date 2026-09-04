"""第 6 课的可执行契约：模型工具调用意图与应用执行权。"""

from pathlib import Path
import importlib.util
import sys

import pytest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_06_tool_calling_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def test_model_tool_text_is_parsed_into_an_intent_without_executing_it() -> None:
    tool_call = main.parse_tool_call(
        '{"tool_name": "add", "arguments": {"left": 2, "right": 3}}'
    )

    assert tool_call == main.ToolCall(
        tool_name="add",
        arguments={"left": 2, "right": 3},
    )


def test_application_executes_the_read_only_add_tool() -> None:
    result = main.execute_tool_call(
        main.ToolCall(
            tool_name="add",
            arguments={"left": 2, "right": 3},
        )
    )

    assert result == 5


def test_application_rejects_an_unknown_tool_instead_of_executing_it() -> None:
    with pytest.raises(ValueError, match="不支持的工具"):
        main.execute_tool_call(
            main.ToolCall(
                tool_name="delete_file",
                arguments={"path": "important.txt"},
            )
        )
