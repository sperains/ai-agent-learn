from dataclasses import dataclass


class RetryableToolError(Exception):
    pass


class NonRetryableToolError(Exception):
    pass


@dataclass(frozen=True)
class ToolResult:
    success: bool
    content: str
    attempts: int


def run_tool_with_retry(tool, max_attempts: int) -> ToolResult:
    for attempt in range(1, max_attempts + 1):
        try:
            content = tool()
            return ToolResult(True, content, attempt)

        except NonRetryableToolError as error:
            return ToolResult(False, str(error), attempt)

        except RetryableToolError as error:
            if attempt == max_attempts:
                return ToolResult(False, str(error), attempt)

    raise ValueError("最大尝试次数必须大于 0")
