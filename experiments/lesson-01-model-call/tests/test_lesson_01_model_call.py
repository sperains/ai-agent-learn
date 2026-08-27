"""第 1 课的可执行契约：模型调用的输入、输出与可替换性。"""

from pathlib import Path
import importlib.util
import sys

import pytest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
MODULE_NAME = "lesson_01_model_call_main"
MODULE_PATH = EXPERIMENT_ROOT / "src" / "main.py"
module_spec = importlib.util.spec_from_file_location(MODULE_NAME, MODULE_PATH)
assert module_spec is not None and module_spec.loader is not None
main = importlib.util.module_from_spec(module_spec)
sys.modules[MODULE_NAME] = main
module_spec.loader.exec_module(main)



def test_fixed_model_returns_its_configured_response() -> None:
    """非空消息会产生初始化时约定的固定响应。"""
    model = main.FixedResponseModel(response="这是固定响应")

    result = model.generate([main.Message(role="user", content="你好")])

    assert result == "这是固定响应"


def test_model_rejects_empty_messages() -> None:
    """空消息不是一次有效模型调用，必须明确失败。"""
    model = main.FixedResponseModel(response="不会被返回")

    with pytest.raises(ValueError, match="消息不能为空"):
        model.generate([])


def test_application_uses_model_contract_not_fixed_model_details() -> None:
    """应用函数只调用 generate，因此任何同契约对象都能被替换进来。"""

    class SpyModel:
        def __init__(self) -> None:
            self.received_messages: list[main.Message] | None = None

        def generate(self, messages: list[main.Message]) -> str:
            self.received_messages = messages
            return "来自替代模型的响应"

    model = SpyModel()
    messages = [main.Message(role="user", content="北京天气如何？")]

    result = main.generate_response(model, messages)

    assert result == "来自替代模型的响应"
    assert model.received_messages == messages
