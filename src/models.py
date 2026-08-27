from dataclasses import dataclass


@dataclass
class SQLResponse:
    question: str
    sql: str
    answer: str
    success: bool
    error: str | None = None
