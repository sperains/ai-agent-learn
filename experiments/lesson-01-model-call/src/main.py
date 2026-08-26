from dataclasses import dataclass
from typing import Protocol

@dataclass(frozen=True)
class Message:
    role: str
    content: str


class Model(Protocol):
    def generate(self, messages: list[Message]) -> str:
        """根据消息生成一段文本响应"""

class FixedResponseModel:

    def __init__(self, response: str) -> None:
        self.response = response

    def generate(self, messages: list[Message]) -> str:
        if not messages:
            raise ValueError('消息不能为空')
        return self.response



def generate_response(model, messages: list[Message]):
    return model.generate(messages)


model = FixedResponseModel('我是固定输出')
generate_response(model, [Message("user", "你好")])
