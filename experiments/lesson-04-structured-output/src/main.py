import json
from dataclasses import dataclass


@dataclass(frozen=True)
class TaskClassification:
    urgent: bool
    category: str


def parse_task_classification(response_text: str) -> TaskClassification:
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError as error:
        raise ValueError("模型响应不是有效 JSON") from error

    if not isinstance(data, dict):
        raise ValueError("模型响应必须是 JSON 对象")

    urgent = data.get("urgent")

    if type(urgent) is not bool:
        raise ValueError("urgent 必须是布尔值")

    category = data.get("category")

    if category not in {"bug", "question"}:
        raise ValueError("category 必须是 bug 或 question")

    return TaskClassification(urgent=urgent, category=category)
