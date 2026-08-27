from langchain_core.language_models import BaseChatModel


def generate_answer(question: str, sql: str, result: str, llm: BaseChatModel) -> str:

    prompt = f"""
You are an AI database assistant.

Answer the user's question using the SQL query result.

User Question:
{question}

Executed SQL:
{sql}

Database Result:
{result}

Rules:
- Answer only based on the database result.
- Be concise and clear.
- Format the answer nicely when multiple rows are returned.
- Do not mention information that is not present in the result.
- Do not invent data.
"""

    response = llm.invoke(prompt)

    return response.content.strip()
