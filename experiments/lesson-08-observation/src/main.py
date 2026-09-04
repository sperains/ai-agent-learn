from dataclasses import dataclass
from collections.abc import Callable


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    arguments: dict[str, object]


def run_tool_conversation(model, user_content: str) -> str:
    messages = [Message(role="user", content=user_content)]

    first_response = model.respond(messages)

    if not isinstance(first_response, ToolCall):
        return first_response

    tool_result = execute_add(first_response)

    messages.append(Message(role="tool", content=str(tool_result)))

    final_response = model.respond(messages)

    if not isinstance(final_response, str):
        raise ValueError("工具结果回传后需要最终文本回答")

    return final_response


def execute_add(tool_call: ToolCall) -> int | float:
    if tool_call.tool_name != "add":
        raise ValueError("不支持的工具")

    left = tool_call.arguments["left"]
    right = tool_call.arguments["right"]

    return left + right
