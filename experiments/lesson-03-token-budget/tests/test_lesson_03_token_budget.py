"""第 3 课的可执行契约：上下文 Token 预算。"""

from pathlib import Path
import importlib.util
import sys

import pytest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_03_token_budget_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)


def test_request_fits_when_input_and_reserved_output_are_within_limit() -> None:
    budget = main.ContextBudget(context_limit=100, output_reserve=30)

    can_send = budget.can_send(
        system_tokens=15,
        history_tokens=30,
        current_user_tokens=20,
    )

    assert can_send is True


def test_request_does_not_fit_when_history_exceeds_its_budget() -> None:
    budget = main.ContextBudget(context_limit=100, output_reserve=30)

    can_send = budget.can_send(
        system_tokens=15,
        history_tokens=40,
        current_user_tokens=20,
    )

    assert can_send is False


def test_remaining_history_budget_reserves_space_for_output_and_current_input() -> None:
    budget = main.ContextBudget(context_limit=100, output_reserve=30)

    remaining = budget.remaining_history_tokens(
        system_tokens=15,
        current_user_tokens=20,
    )

    assert remaining == 35


def test_budget_rejects_output_reserve_larger_than_context_limit() -> None:
    with pytest.raises(ValueError, match="输出预留不能超过上下文上限"):
        main.ContextBudget(context_limit=100, output_reserve=101)
