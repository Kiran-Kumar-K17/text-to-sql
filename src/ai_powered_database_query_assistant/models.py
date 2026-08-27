from dataclasses import dataclass


@dataclass
class SQLResponse:
    question: str
    sql: str
    answer: str
    success: bool
    error: str | None = None
    original_sql: str | None = None
    was_fixed: bool = False
