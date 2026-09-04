"""第 11 课的可执行契约：工具失败、有限重试与 Observation。"""

from pathlib import Path
import importlib.util
import sys


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_11_tool_retry_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def test_retryable_failure_can_succeed_on_a_later_attempt() -> None:
    attempts = 0

    def flaky_tool() -> str:
        nonlocal attempts
        attempts += 1
        if attempts == 1:
            raise main.RetryableToolError("临时超时")
        return "5"

    result = main.run_tool_with_retry(flaky_tool, max_attempts=2)

    assert result.success is True
    assert result.content == "5"
    assert result.attempts == 2


def test_non_retryable_failure_stops_without_a_second_attempt() -> None:
    attempts = 0

    def invalid_tool() -> str:
        nonlocal attempts
        attempts += 1
        raise main.NonRetryableToolError("缺少参数 left")

    result = main.run_tool_with_retry(invalid_tool, max_attempts=2)

    assert result.success is False
    assert result.content == "缺少参数 left"
    assert result.attempts == 1


def test_exhausted_retryable_failure_becomes_a_failure_observation() -> None:
    def unavailable_tool() -> str:
        raise main.RetryableToolError("服务暂时不可用")

    result = main.run_tool_with_retry(unavailable_tool, max_attempts=2)

    assert result.success is False
    assert result.content == "服务暂时不可用"
    assert result.attempts == 2
