from dotenv import load_dotenv

from src.database import get_database
from src.llm import get_llm
from src.assistant import SQLAssistant

load_dotenv()


db = get_database("data/Chinook.db")

llm = get_llm()


assistant = SQLAssistant(db=db, llm=llm)


questions = [
    "How many customers are there?",
    "Show all customers from Germany.",
    "Which country has the highest number of customers?",
    "Show the top 5 most expensive tracks.",
    "List all albums created by AC/DC.",
    "Which artist has the most tracks?",
    "Show the top 5 customers by total spending.",
    "Which music genre has the highest number of tracks?",
    "Which artist generated the highest revenue from track sales?",
    "Show the top 5 countries by total revenue.",
]

for i, question in enumerate(questions, start=1):

    print("\n" + "=" * 100)
    print(f"QUESTION {i}: {question}")
    print("=" * 100)

    response = assistant.ask(question)

    print(f"\nQuestion:\n{response.question}")

    print(f"\nSQL:\n{response.sql}")

    print(f"\nAnswer:\n{response.answer}")

    print(f"\nSuccess:\n{response.success}")
