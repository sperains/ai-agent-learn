from enum import Enum


class ErrorCategory(Enum):
    TIMEOUT = "timeout"
    RATE_LIMIT = "rate_limit"
    CLIENT = "client"
    SERVER = "server"
    UNKNOWN = "unknown"


class HttpError(Exception):
    def __init__(self, status_code: int) -> None:
        self.status_code = status_code
        super().__init__(f"HTTP 状态码: {status_code}")


def classify_error(error: Exception) -> ErrorCategory:
    if isinstance(error, TimeoutError):
        return ErrorCategory.TIMEOUT

    if isinstance(error, HttpError):
        if error.status_code == 429:
            return ErrorCategory.RATE_LIMIT
        if 400 <= error.status_code < 500:
            return ErrorCategory.CLIENT
        if 500 <= error.status_code < 600:
            return ErrorCategory.SERVER

    return ErrorCategory.UNKNOWN


def is_retryable(category: ErrorCategory) -> bool:
    return category in {
        ErrorCategory.TIMEOUT,
        ErrorCategory.RATE_LIMIT,
        ErrorCategory.SERVER,
    }
