from dataclasses import dataclass


@dataclass(frozen=True)
class ContextBudget:
    context_limit: int
    output_reserve: int

    def __post_init__(self) -> None:
        if self.output_reserve > self.context_limit:
            raise ValueError("输出预留不能超过上下文上限")

    def can_send(
        self, system_tokens: int, history_tokens: int, current_user_tokens: int
    ) -> bool:
        total_tokens = (
            system_tokens + history_tokens + current_user_tokens + self.output_reserve
        )
        return total_tokens <= self.context_limit

    def remaining_history_tokens(
        self, system_tokens: int, current_user_tokens: int
    ) -> int:
        return max(
            0,
            self.context_limit
            - self.output_reserve
            - system_tokens
            - current_user_tokens,
        )


ctx = ContextBudget(100, 30)
print(ctx.can_send(15, 30, 20))
print(ctx.remaining_history_tokens(15, 20))
