from unittest.mock import Mock

from ai_powered_database_query_assistant.sql_fixer import fix_sql


def test_fix_sql_returns_corrected_sql():

    # Mock LLM response
    mock_response = Mock()
    mock_response.content = """
    SELECT *
    FROM Customer;
    """

    # Mock LLM
    mock_llm = Mock()
    mock_llm.invoke.return_value = mock_response

    result = fix_sql(
        question="Show all customers",
        schema="Customer(CustomerId, FirstName, LastName)",
        failed_sql="SELECT * FROM Customers;",
        error="no such table: Customers",
        llm=mock_llm,
    )

    assert result == "SELECT *\n    FROM Customer;"
