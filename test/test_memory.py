from ai_powered_database_query_assistant.memory import ConversationMemory


def test_add_conversation():
    memory = ConversationMemory()

    memory.add(
        question="How many customers are there?",
        sql="SELECT COUNT(*) FROM Customer;",
        answer="There are 59 customers.",
    )

    assert len(memory.history) == 1


def test_get_context():
    memory = ConversationMemory()

    memory.add(
        question="Show top 5 customers.",
        sql="SELECT * FROM Customer LIMIT 5;",
        answer="Here are the top 5 customers.",
    )

    context = memory.get_context()

    assert "Show top 5 customers." in context
    assert "SELECT * FROM Customer LIMIT 5;" in context


def test_empty_memory():
    memory = ConversationMemory()

    context = memory.get_context()

    assert context == ""
