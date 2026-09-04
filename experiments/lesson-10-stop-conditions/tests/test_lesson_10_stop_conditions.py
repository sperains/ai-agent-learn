"""第 10 课的可执行契约：Agent Loop 的最大步数与终止原因。"""

from pathlib import Path
import importlib.util
import sys

import pytest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_10_stop_conditions_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def test_agent_returns_final_answer_before_reaching_max_steps() -> None:
    class FinalTextModel:
        def respond(self, messages: list[main.Message]) -> main.ToolCall | str:
            return "任务完成。"

    result = main.run_agent(FinalTextModel(), user_content="你好", max_steps=2)

    assert result.answer == "任务完成。"
    assert result.stop_reason is main.StopReason.FINAL_ANSWER


def test_agent_stops_after_max_steps_when_model_keeps_requesting_tools() -> None:
    class RepeatingToolModel:
        def __init__(self) -> None:
            self.request_count = 0

        def respond(self, messages: list[main.Message]) -> main.ToolCall | str:
            self.request_count += 1
            return main.ToolCall(
                tool_name="add",
                arguments={"left": 1, "right": 1},
            )

    model = RepeatingToolModel()

    result = main.run_agent(model, user_content="不断计算", max_steps=2)

    assert result.answer is None
    assert result.stop_reason is main.StopReason.MAX_STEPS
    assert model.request_count == 2


def test_agent_rejects_non_positive_max_steps() -> None:
    with pytest.raises(ValueError, match="最大步数必须大于 0"):
        main.run_agent(object(), user_content="你好", max_steps=0)
