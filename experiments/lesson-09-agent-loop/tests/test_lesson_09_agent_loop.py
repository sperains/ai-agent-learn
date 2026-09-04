"""第 9 课的可执行契约：应用控制最小 Agent Loop。"""

from pathlib import Path
import importlib.util
import sys


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_09_agent_loop_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def test_agent_loop_continues_after_tool_call_and_stops_at_final_text() -> None:
    class ScriptedModel:
        def __init__(self) -> None:
            self.request_count = 0

        def respond(self, messages: list[main.Message]) -> main.ToolCall | str:
            self.request_count += 1
            if self.request_count == 1:
                return main.ToolCall(
                    tool_name="add",
                    arguments={"left": 2, "right": 3},
                )

            assert messages[-1] == main.Message(role="tool", content="5")
            return "2 加 3 等于 5。"

    model = ScriptedModel()

    answer = main.run_agent(model, user_content="请计算 2 加 3。")

    assert answer == "2 加 3 等于 5。"
    assert model.request_count == 2


def test_agent_loop_stops_without_calling_a_tool_when_model_returns_text_first() -> None:
    class FinalTextModel:
        def __init__(self) -> None:
            self.request_count = 0

        def respond(self, messages: list[main.Message]) -> main.ToolCall | str:
            self.request_count += 1
            return "不需要工具。"

    model = FinalTextModel()

    answer = main.run_agent(model, user_content="你好")

    assert answer == "不需要工具。"
    assert model.request_count == 1
