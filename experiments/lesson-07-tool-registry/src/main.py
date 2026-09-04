from dataclasses import dataclass
from collections.abc import Callable


@dataclass(frozen=True)
class ToolCall:
    tool_name: str
    arguments: dict[str, object]


ToolExecutor = Callable[[dict[str, object]], int | float]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolExecutor] = {}

    def register_add(self) -> None:
        self._tools["add"] = self._execute_add

    def execute(self, tool_call: ToolCall) -> int | float:
        tool = self._tools.get(tool_call.tool_name)
        if tool is None:
            raise ValueError("未注册的工具")
        return tool(tool_call.arguments)

    def _execute_add(self, arguments: dict[str, object]) -> int | float:
        left = self._require_number(arguments, "left")
        right = self._require_number(arguments, "right")
        return left + right

    def _require_number(self, arguments: dict[str, object], name: str) -> int | float:
        if name not in arguments:
            raise ValueError(f"缺少参数 {name}")

        value = arguments[name]
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"参数 {name} 必须是数字")

        return value
