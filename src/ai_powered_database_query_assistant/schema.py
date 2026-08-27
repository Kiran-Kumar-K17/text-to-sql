from langchain_community.utilities import SQLDatabase


def get_schema(db: SQLDatabase) -> str:
    return db.get_table_info()
