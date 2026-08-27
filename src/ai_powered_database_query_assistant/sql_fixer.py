from langchain_core.language_models import BaseChatModel


def fix_sql(
    question: str, schema: str, failed_sql: str, error: str, llm: BaseChatModel
) -> str:

    prompt = f"""
You are an expert SQLite SQL developer.

The following SQL query failed.

User Question:
{question}

Database Schema:
{schema}

Failed SQL:
{failed_sql}

Database Error:
{error}

Fix the SQL query.

Rules:
- Use only tables and columns from the schema.
- Generate valid SQLite SQL.
- Return only the corrected SQL query.
- Do not include explanations.
- Do not use Markdown code blocks.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE statements.
"""

    response = llm.invoke(prompt)

    return response.content.strip()
