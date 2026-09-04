"""第 5 课的可执行契约：请求失败分类与重试判断。"""

from pathlib import Path
import importlib.util
import sys


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_05_http_errors_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def test_timeout_is_retryable_because_the_remote_outcome_is_unknown() -> None:
    category = main.classify_error(TimeoutError("请求超时"))

    assert category is main.ErrorCategory.TIMEOUT
    assert main.is_retryable(category) is True


def test_rate_limit_is_retryable() -> None:
    category = main.classify_error(main.HttpError(status_code=429))

    assert category is main.ErrorCategory.RATE_LIMIT
    assert main.is_retryable(category) is True


def test_bad_request_is_not_retryable_without_changing_the_request() -> None:
    category = main.classify_error(main.HttpError(status_code=400))

    assert category is main.ErrorCategory.CLIENT
    assert main.is_retryable(category) is False


def test_server_error_is_retryable() -> None:
    category = main.classify_error(main.HttpError(status_code=503))

    assert category is main.ErrorCategory.SERVER
    assert main.is_retryable(category) is True
