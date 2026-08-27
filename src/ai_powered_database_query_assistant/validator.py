import re


def validate_sql(sql_query: str) -> bool:
    sql = sql_query.strip()

    if not sql:
        return False

    # Remove trailing semicolon
    sql = sql.rstrip(";").strip()

    upper_sql = sql.upper()

    # Allow only read-only queries
    if not (upper_sql.startswith("SELECT") or upper_sql.startswith("WITH")):
        return False

    # Block dangerous SQL keywords as whole words
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
        pattern = rf"\b{keyword}\b"

        if re.search(pattern, upper_sql):
            return False

    # Prevent multiple SQL statements
    # A semicolon should only be allowed at the end
    if ";" in sql:
        return False

    return True
