from dataclasses import dataclass
import json


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    arguments: dict[str, object]


def parse_tool_call(response_text: str) -> ToolCall:
    data = json.loads(response_text)

    return ToolCall(tool_name=data["tool_name"], arguments=data["arguments"])


def execute_tool_call(tool_call: ToolCall) -> int:
    if tool_call.tool_name != "add":
        raise ValueError("不支持的工具")

    left = tool_call.arguments["left"]
    right = tool_call.arguments["right"]
    return left + right
