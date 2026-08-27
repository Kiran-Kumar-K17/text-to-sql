from langchain_community.utilities import SQLDatabase


def execute_sql(db: SQLDatabase, sql_query: str) -> str:
    return db.run(sql_query)
