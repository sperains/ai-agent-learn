from dataclasses import dataclass
from enum import Enum


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    arguments: dict[str, object]


class StopReason(Enum):
    FINAL_ANSWER = "final_answer"
    MAX_STEPS = "max_steps"


@dataclass(frozen=True)
class AgentResult:
    answer: str | None
    stop_reason: StopReason


def run_agent(model, user_content: str, max_steps: int) -> AgentResult:
    if max_steps <= 0:
        raise ValueError("最大步数必须大于 0")

    messages = [Message(role="user", content=user_content)]

    for _ in range(max_steps):
        response = model.respond(messages)
        if isinstance(response, str):
            return AgentResult(answer=response, stop_reason=StopReason.FINAL_ANSWER)

        result = execute_add(response)
        messages.append(Message(role="tool", content=str(result)))

    return AgentResult(answer=None, stop_reason=StopReason.MAX_STEPS)


def execute_add(tool_call: ToolCall) -> int | float:
    if tool_call.tool_name != "add":
        raise ValueError("不支持的工具")

    return tool_call.arguments["left"] + tool_call.arguments["right"]
