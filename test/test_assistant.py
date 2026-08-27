from unittest.mock import Mock, patch

from ai_powered_database_query_assistant.assistant import SQLAssistant

# ============================================================
# Helper function
# Creates SQLAssistant with mocked database and LLM
# ============================================================


def create_assistant():
    mock_db = Mock()
    mock_llm = Mock()

    with patch(
        "ai_powered_database_query_assistant.assistant.get_schema",
        return_value="mock schema",
    ):
        assistant = SQLAssistant(
            db=mock_db,
            llm=mock_llm,
        )

    return assistant


# ============================================================
# 1. SUCCESSFUL QUERY
# ============================================================


@patch("ai_powered_database_query_assistant.assistant.generate_answer")
@patch("ai_powered_database_query_assistant.assistant.execute_sql")
@patch("ai_powered_database_query_assistant.assistant.validate_sql")
@patch("ai_powered_database_query_assistant.assistant.generate_sql")
@patch("ai_powered_database_query_assistant.assistant.validate_question")
def test_successful_query(
    mock_validate_question,
    mock_generate_sql,
    mock_validate_sql,
    mock_execute_sql,
    mock_generate_answer,
):
    assistant = create_assistant()

    # Mock question validation
    mock_validate_question.return_value = True

    # Mock generated SQL
    mock_generate_sql.return_value = "SELECT COUNT(*) FROM Customer;"

    # SQL is safe
    mock_validate_sql.return_value = True

    # Mock database result
    mock_execute_sql.return_value = "[(59,)]"

    # Mock final answer
    mock_generate_answer.return_value = "There are 59 customers."

    response = assistant.ask("How many customers are there?")

    assert response.success is True
    assert response.answer == "There are 59 customers."
    assert response.sql == "SELECT COUNT(*) FROM Customer;"
    assert response.was_fixed is False


# ============================================================
# 2. INVALID QUESTION
# ============================================================


@patch("ai_powered_database_query_assistant.assistant.validate_question")
def test_invalid_question(mock_validate_question):

    assistant = create_assistant()

    # Question is invalid
    mock_validate_question.return_value = False

    response = assistant.ask("q")

    assert response.success is False

    assert response.sql == ""

    assert response.answer == (
        "Please ask a clear question that can be answered " "using the database."
    )

    assert response.error == ("Invalid or unclear question.")


# ============================================================
# 3. UNSAFE SQL
# ============================================================


@patch("ai_powered_database_query_assistant.assistant.validate_sql")
@patch("ai_powered_database_query_assistant.assistant.generate_sql")
@patch("ai_powered_database_query_assistant.assistant.validate_question")
def test_unsafe_sql(
    mock_validate_question,
    mock_generate_sql,
    mock_validate_sql,
):

    assistant = create_assistant()

    # Valid question
    mock_validate_question.return_value = True

    # Dangerous SQL generated
    mock_generate_sql.return_value = "DELETE FROM Customer;"

    # SQL validation fails
    mock_validate_sql.return_value = False

    response = assistant.ask("Delete all customers")

    assert response.success is False

    assert response.sql == ("DELETE FROM Customer;")

    assert response.answer == ("Generated SQL was unsafe or invalid.")

    assert response.error == ("SQL validation failed.")


# ============================================================
# 4. SQL FAILS -> FIX SQL -> SUCCESS
# ============================================================


@patch("ai_powered_database_query_assistant.assistant.generate_answer")
@patch("ai_powered_database_query_assistant.assistant.execute_sql")
@patch("ai_powered_database_query_assistant.assistant.validate_sql")
@patch("ai_powered_database_query_assistant.assistant.fix_sql")
@patch("ai_powered_database_query_assistant.assistant.generate_sql")
@patch("ai_powered_database_query_assistant.assistant.validate_question")
def test_sql_fix_success(
    mock_validate_question,
    mock_generate_sql,
    mock_fix_sql,
    mock_validate_sql,
    mock_execute_sql,
    mock_generate_answer,
):

    assistant = create_assistant()

    # Valid question
    mock_validate_question.return_value = True

    # Initial SQL has wrong table name
    mock_generate_sql.return_value = "SELECT * FROM Customers;"

    # Both original and fixed SQL pass validation
    mock_validate_sql.return_value = True

    # First execution fails
    # Second execution succeeds
    mock_execute_sql.side_effect = [
        Exception("no such table: Customers"),
        "[(1, 'John')]",
    ]

    # SQL fixer generates correct SQL
    mock_fix_sql.return_value = "SELECT * FROM Customer;"

    # Final answer
    mock_generate_answer.return_value = "Here is the customer."

    response = assistant.ask("Show customers")

    assert response.success is True

    assert response.was_fixed is True

    assert response.sql == ("SELECT * FROM Customer;")

    assert response.original_sql == ("SELECT * FROM Customers;")

    assert response.answer == ("Here is the customer.")

    # Ensure fixer was called once
    mock_fix_sql.assert_called_once()


# ============================================================
# 5. FIXED SQL ALSO FAILS
# ============================================================


@patch("ai_powered_database_query_assistant.assistant.execute_sql")
@patch("ai_powered_database_query_assistant.assistant.validate_sql")
@patch("ai_powered_database_query_assistant.assistant.fix_sql")
@patch("ai_powered_database_query_assistant.assistant.generate_sql")
@patch("ai_powered_database_query_assistant.assistant.validate_question")
def test_fixed_sql_execution_fails(
    mock_validate_question,
    mock_generate_sql,
    mock_fix_sql,
    mock_validate_sql,
    mock_execute_sql,
):

    assistant = create_assistant()

    # Valid question
    mock_validate_question.return_value = True

    # Initial SQL
    mock_generate_sql.return_value = "SELECT * FROM WrongTable;"

    # SQL passes safety validation
    mock_validate_sql.return_value = True

    # First execution fails
    # Fixed SQL execution also fails
    mock_execute_sql.side_effect = [
        Exception("no such table: WrongTable"),
        Exception("still invalid SQL"),
    ]

    # SQL fixer tries another query
    mock_fix_sql.return_value = "SELECT * FROM AnotherWrongTable;"

    response = assistant.ask("Show something")

    assert response.success is False

    assert response.answer == ("SQL execution failed.")

    assert response.error == ("still invalid SQL")
