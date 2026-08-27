from langchain_community.utilities import SQLDatabase


def get_database(db_path: str):
    db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
    return db
