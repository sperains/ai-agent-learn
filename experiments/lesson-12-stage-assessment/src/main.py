from dataclasses import dataclass


@dataclass(frozen=True)
class AgentResult:
    answer: str | None
    reason: str


def run_agent(script: list[object], max_steps: int) -> AgentResult:
    for step, event in enumerate(script[:max_steps]):
        if isinstance(event, str):
            return AgentResult(event, "final_answer")

        tool_name = event["tool_name"]
        arguments = event["arguments"]

        if tool_name == "temporarily_unavailable":
            return AgentResult(None, "tool_failure")

        if tool_name != "add":
            return AgentResult(None, "unknown_tool")

        left = arguments.get("left")
        right = arguments.get("right")

        if (
            isinstance(left, bool)
            or isinstance(right, bool)
            or not isinstance(left, (int, float))
            or not isinstance(right, (int, float))
        ):
            return AgentResult(None, "invalid_arguments")

        _ = left + right

    return AgentResult(None, "max_steps")
