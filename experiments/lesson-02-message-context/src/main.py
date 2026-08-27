from dataclasses import dataclass, field


@dataclass(frozen=True)
class Message:
    role: str
    content: str



@dataclass
class Conversation:

    system_instruction: str
    history: list[Message] = field(default_factory=list)


    def record_turn(self, user_content, assistant_content: str) -> None:
        self.history.append(Message(role="user", content=user_content))
        self.history.append(Message(role="assistant", content=assistant_content))


    def build_request(self, current_user_content) -> list[Message]:
        if not current_user_content:
            raise ValueError('当前用户消息不能为空')

        return [
            Message(role="system", content=self.system_instruction),
            *self.history,
            Message(role="user", content=current_user_content)
        ]


c = Conversation('你是一个学习助手')
c.record_turn("我想学习AI-Agent", "好的, 我知道了")
result = c.build_request('下一步应该怎么办')

