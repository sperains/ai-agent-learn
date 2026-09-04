"""第 8 课的可执行契约：工具结果作为 Observation 回传。"""

from pathlib import Path
import importlib.util
import sys

import pytest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_08_observation_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def test_tool_result_is_returned_to_model_before_final_answer() -> None:
    class TwoStepModel:
        def __init__(self) -> None:
            self.requests: list[list[main.Message]] = []

        def respond(self, messages: list[main.Message]) -> main.ToolCall | str:
            self.requests.append(messages.copy())
            if len(self.requests) == 1:
                return main.ToolCall(
                    tool_name="add",
                    arguments={"left": 2, "right": 3},
                )
            return "2 加 3 等于 5。"

    model = TwoStepModel()

    answer = main.run_tool_conversation(
        model,
        user_content="请计算 2 加 3。",
    )

    assert answer == "2 加 3 等于 5。"
    assert model.requests[1][-1] == main.Message(role="tool", content="5")


def test_tool_failure_stops_before_a_second_model_call() -> None:
    class UnknownToolModel:
        def __init__(self) -> None:
            self.call_count = 0

        def respond(self, messages: list[main.Message]) -> main.ToolCall | str:
            self.call_count += 1
            return main.ToolCall(tool_name="delete_file", arguments={})

    model = UnknownToolModel()

    with pytest.raises(ValueError, match="不支持的工具"):
        main.run_tool_conversation(model, user_content="删除文件")

    assert model.call_count == 1
