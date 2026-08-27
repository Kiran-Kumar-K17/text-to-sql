import pytest
from dotenv import load_dotenv

from ai_powered_database_query_assistant.assistant import SQLAssistant
from ai_powered_database_query_assistant.database import get_database
from ai_powered_database_query_assistant.llm import get_llm


@pytest.fixture(scope="module")
def assistant():
    load_dotenv()

    db = get_database("data/Chinook.db")
    llm = get_llm()

    return SQLAssistant(
        db=db,
        llm=llm,
    )


def test_customer_count(assistant):
    response = assistant.ask("How many customers are there?")

    assert response.success is True
    assert response.sql
    assert "SELECT" in response.sql.upper()
    assert "59" in response.answer


def test_artist_with_most_tracks(assistant):
    response = assistant.ask("Which artist has the most tracks?")

    assert response.success is True
    assert response.sql
    assert "SELECT" in response.sql.upper()

    # LLM formatting may use different Unicode spaces
    assert "Iron" in response.answer
    assert "Maiden" in response.answer


def test_invalid_question(assistant):
    response = assistant.ask("asdfgh")

    assert response.success is False
