from ai_powered_database_query_assistant.validator import validate_sql


def test_valid_select_query():
    assert validate_sql("SELECT * FROM Customer;") is True


def test_valid_with_query():
    sql = """
    WITH customer_count AS (
        SELECT COUNT(*) AS count
        FROM Customer
    )
    SELECT * FROM customer_count;
    """

    assert validate_sql(sql) is True


def test_delete_query():
    assert validate_sql("DELETE FROM Customer;") is False


def test_update_query():
    assert validate_sql("UPDATE Customer SET FirstName = 'Test';") is False


def test_drop_query():
    assert validate_sql("DROP TABLE Customer;") is False


def test_multiple_queries():
    assert validate_sql("SELECT * FROM Customer; DELETE FROM Customer;") is False


def test_empty_query():
    assert validate_sql("") is False


def test_non_select_query():
    assert validate_sql("INSERT INTO Customer VALUES (1);") is False


def test_pragma_query():
    assert validate_sql("PRAGMA table_info(Customer);") is False


def test_attach_query():
    assert validate_sql("ATTACH DATABASE 'test.db' AS test;") is False
