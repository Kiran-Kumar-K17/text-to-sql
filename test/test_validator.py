from ai_powered_database_query_assistant.validator import validate_sql


def test_valid_select_query():
    sql = "SELECT * FROM Customer;"

    assert validate_sql(sql) is True


def test_delete_query():
    sql = "DELETE FROM Customer;"

    assert validate_sql(sql) is False


def test_update_query():
    sql = "UPDATE Customer SET FirstName = 'Test';"

    assert validate_sql(sql) is False


def test_drop_query():
    sql = "DROP TABLE Customer;"

    assert validate_sql(sql) is False


def test_multiple_queries():
    sql = "SELECT * FROM Customer; DELETE FROM Customer;"

    assert validate_sql(sql) is False
