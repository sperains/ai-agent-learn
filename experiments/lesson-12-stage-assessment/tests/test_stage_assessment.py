"""第一阶段集成验收：最小 Agent 运行时的四个核心结果。"""

from pathlib import Path
import importlib.util
import sys


ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("lesson_12_main", ROOT / "src" / "main.py")
assert spec is not None and spec.loader is not None
main = importlib.util.module_from_spec(spec)
sys.modules["lesson_12_main"] = main
spec.loader.exec_module(main)


def test_direct_final_answer_completes() -> None:
    result = main.run_agent(["完成"], max_steps=2)
    assert result.answer == "完成"
    assert result.reason == "final_answer"


def test_invalid_tool_arguments_are_rejected() -> None:
    result = main.run_agent(
        [{"tool_name": "add", "arguments": {"left": 2, "right": "three"}}],
        max_steps=2,
    )
    assert result.answer is None
    assert result.reason == "invalid_arguments"


def test_retryable_tool_failure_becomes_failure_result_after_retry() -> None:
    result = main.run_agent(
        [{"tool_name": "temporarily_unavailable", "arguments": {}}],
        max_steps=2,
    )
    assert result.answer is None
    assert result.reason == "tool_failure"


def test_repeated_valid_tool_calls_stop_at_max_steps() -> None:
    call = {"tool_name": "add", "arguments": {"left": 1, "right": 1}}
    result = main.run_agent([call, call, call], max_steps=2)
    assert result.answer is None
    assert result.reason == "max_steps"
