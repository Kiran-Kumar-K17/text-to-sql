def validate_question(question: str, llm) -> bool:

    question = question.strip()

    # Basic validation
    if not question or len(question) < 5:
        return False

    prompt = f"""
You are validating user input for a Text-to-SQL assistant.

The assistant can only answer meaningful questions that can potentially
be answered using a database.

Determine whether the following user input is a meaningful database-related
question.

Return ONLY:

YES

or

NO

User Input:
{question}
"""

    response = llm.invoke(prompt)

    answer = response.content.strip().upper()

    return answer == "YES"
