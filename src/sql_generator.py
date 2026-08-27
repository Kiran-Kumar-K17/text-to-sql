from langchain_core.language_models import BaseChatModel


def generate_sql(question: str, schema: str, llm: BaseChatModel) -> str:

    prompt = f"""
You are an expert SQLite SQL generator.

Given the database schema and user question,
generate a correct SQLite SQL query.

Database Schema:
{schema}

User Question:
{question}

Rules:
- Use only the tables and columns provided in the schema.
- Generate SQLite-compatible SQL.
- Return only the SQL query.
- Do not include explanations.
- Do not use Markdown code blocks.
- Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE statements.
"""

    response = llm.invoke(prompt)

    return response.content.strip()
