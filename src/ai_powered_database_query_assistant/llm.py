from langchain_groq import ChatGroq

from ai_powered_database_query_assistant.config import MODEL_NAME, TEMPERATURE


def get_llm():
    return ChatGroq(
        model=MODEL_NAME,
        temperature=TEMPERATURE,
    )
