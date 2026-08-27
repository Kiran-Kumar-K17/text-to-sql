from ai_powered_database_query_assistant.config import MAX_HISTORY


class ConversationMemory:

    def __init__(self, max_history: int = 5):
        self.history = []
        self.max_history = MAX_HISTORY

    def add(self, question: str, sql: str, answer: str):
        self.history.append({"question": question, "sql": sql, "answer": answer})
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def get_context(self) -> str:

        if not self.history:
            return ""

        context = ""

        for item in self.history:
            context += f"""
                    Previous Question:
                    {item["question"]}

                    Previous SQL:
                    {item["sql"]}

                    Previous Answer:
                    {item["answer"]}
"""

        return context
