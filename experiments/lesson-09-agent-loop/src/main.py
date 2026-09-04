from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    role: str
    content: str


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    arguments: dict[str, object]


def run_agent(model, user_content: str) -> str:
    messages = [Message(role="user", content=user_content)]

    while True:
        response = model.respond(messages)

        if isinstance(response, str):
            return response

        tool_result = execute_add(response)

        messages.append(Message(role="tool", content=str(tool_result)))


def execute_add(tool_call: ToolCall) -> int | float:
    if tool_call.tool_name != "add":
        raise ValueError("不支持的工具")

    left = tool_call.arguments["left"]
    right = tool_call.arguments["right"]
    return left + right
