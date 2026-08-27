from ai_powered_database_query_assistant.database import get_database
from ai_powered_database_query_assistant.executor import execute_sql


def test_execute_valid_query():
    db = get_database("data/Chinook.db")

    result = execute_sql(db, "SELECT COUNT(*) AS customer_count FROM Customer;")

    assert result is not None


def test_customer_count():
    db = get_database("data/Chinook.db")

    result = execute_sql(db, "SELECT COUNT(*) FROM Customer;")

    assert result == "[(59,)]"
