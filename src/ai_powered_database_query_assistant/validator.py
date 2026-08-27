def validate_sql(sql_query: str) -> bool:

    sql = sql_query.strip()
    upper_sql = sql.upper()

    # Allow only read queries
    if not (upper_sql.startswith("SELECT") or upper_sql.startswith("WITH")):
        return False

    # Block dangerous SQL operations
    forbidden_keywords = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "ALTER",
        "CREATE",
        "REPLACE",
        "TRUNCATE",
        "ATTACH",
        "DETACH",
        "PRAGMA",
    ]

    for keyword in forbidden_keywords:
        if keyword in upper_sql:
            return False

    # Prevent multiple SQL statements
    statements = [
        statement.strip() for statement in sql.split(";") if statement.strip()
    ]

    if len(statements) != 1:
        return False

    return True
