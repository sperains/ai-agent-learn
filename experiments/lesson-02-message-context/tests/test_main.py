"""第 2 课的可执行契约：角色、历史与本轮上下文。"""

from pathlib import Path
import sys

import pytest


EXPERIMENT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EXPERIMENT_ROOT / "src"))

import main  # noqa: E402


def test_request_contains_system_history_and_current_user_message_in_order() -> None:
    conversation = main.Conversation(system_instruction="你是一名简洁的学习助手。")
    conversation.record_turn(
        user_content="我在学习模型调用。",
        assistant_content="模型调用是一次输入到输出的请求。",
    )

    request = conversation.build_request(current_user_content="那空消息怎么办？")

    assert request == [
        main.Message(role="system", content="你是一名简洁的学习助手。"),
        main.Message(role="user", content="我在学习模型调用。"),
        main.Message(role="assistant", content="模型调用是一次输入到输出的请求。"),
        main.Message(role="user", content="那空消息怎么办？"),
    ]


def test_record_turn_keeps_both_user_and_assistant_messages() -> None:
    conversation = main.Conversation(system_instruction="遵守事实。")

    conversation.record_turn(user_content="你好", assistant_content="你好，我能帮你学习。")

    assert conversation.history == [
        main.Message(role="user", content="你好"),
        main.Message(role="assistant", content="你好，我能帮你学习。"),
    ]


def test_first_request_contains_system_and_current_user_without_history() -> None:
    conversation = main.Conversation(system_instruction="回答要简洁。")

    request = conversation.build_request(current_user_content="什么是上下文？")

    assert request == [
        main.Message(role="system", content="回答要简洁。"),
        main.Message(role="user", content="什么是上下文？"),
    ]
    assert conversation.history == []


def test_request_rejects_empty_current_user_message() -> None:
    conversation = main.Conversation(system_instruction="回答要简洁。")

    with pytest.raises(ValueError, match="当前用户消息不能为空"):
        conversation.build_request(current_user_content="")
