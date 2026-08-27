from dotenv import load_dotenv

from ai_powered_database_query_assistant.database import get_database
from ai_powered_database_query_assistant.llm import get_llm
from ai_powered_database_query_assistant.assistant import SQLAssistant
from ai_powered_database_query_assistant.config import DB_PATH

load_dotenv()


db = get_database(DB_PATH)

llm = get_llm()

assistant = SQLAssistant(db=db, llm=llm)


print("=" * 60)
print("Welcome to the Text-to-SQL Assistant")
print("Type 'exit' or 'quit' to stop.")
print("=" * 60)


while True:

    question = input("\nAsk a question: ")

    if question.lower() in ["exit", "quit"]:
        print("\nGoodbye! 👋")
        break

    if not question.strip():
        print("Please enter a question.")
        continue

    response = assistant.ask(question)

    print("\n" + "=" * 60)

    print("\nGenerated SQL:")
    print(response.sql)

    print("\nAnswer:")
    print(response.answer)

    print(f"\nSuccess: {response.success}")

    if response.was_fixed:
        print("Note: The original SQL was automatically fixed.")

    if response.error:
        print(f"\nError: {response.error}")

    print("=" * 60)
