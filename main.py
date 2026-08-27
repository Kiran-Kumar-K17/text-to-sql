from dotenv import load_dotenv

from src.database import get_database
from src.llm import get_llm
from src.assistant import SQLAssistant

load_dotenv()


db = get_database("data/Chinook.db")

llm = get_llm()


assistant = SQLAssistant(db=db, llm=llm)


questions = [
    "Show the top 5 customers by total spending.",
    "Show only the first 2.",
    "What country are they from?",
]

for question in questions:

    response = assistant.ask(question)

    print("\n" + "=" * 60)
    print(f"Question: {response.question}")
    print(f"\nSQL:\n{response.sql}")
    print(f"\nAnswer:\n{response.answer}")
