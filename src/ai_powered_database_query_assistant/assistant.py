from langchain_community.utilities import SQLDatabase
from langchain_core.language_models import BaseChatModel

from ai_powered_database_query_assistant.schema import get_schema
from ai_powered_database_query_assistant.sql_generator import generate_sql
from ai_powered_database_query_assistant.validator import validate_sql
from ai_powered_database_query_assistant.executor import execute_sql
from ai_powered_database_query_assistant.sql_fixer import fix_sql
from ai_powered_database_query_assistant.answer_generator import generate_answer
from ai_powered_database_query_assistant.models import SQLResponse
from ai_powered_database_query_assistant.memory import ConversationMemory
from ai_powered_database_query_assistant.question_validator import validate_question
from ai_powered_database_query_assistant.logger import get_logger
from ai_powered_database_query_assistant.config import MAX_SQL_RETRIES


class SQLAssistant:

    def __init__(self, db: SQLDatabase, llm: BaseChatModel):
        self.db = db
        self.llm = llm
        self.schema = get_schema(db)
        self.memory = ConversationMemory()
        self.logger = get_logger(__name__)

    def ask(self, question: str) -> SQLResponse:

        self.logger.info(f"Received question: {question}")

        # Validate question
        if not validate_question(question, self.llm):

            self.logger.warning(f"Invalid question rejected: {question}")

            return SQLResponse(
                question=question,
                sql="",
                answer="Please ask a clear question that can be answered using the database.",
                success=False,
                error="Invalid or unclear question.",
            )

        self.logger.info("Question validation passed")

        # Get conversation context
        context = self.memory.get_context()

        # Generate SQL
        self.logger.info("Generating SQL")

        sql = generate_sql(
            question=question,
            schema=self.schema,
            llm=self.llm,
            context=context,
        )

        self.logger.info(f"Generated SQL: {sql}")

        original_sql = sql
        final_sql = sql

        result = None
        was_fixed = False
        last_error = None

        # Execute SQL with retry mechanism
        for attempt in range(MAX_SQL_RETRIES + 1):

            attempt_number = attempt + 1

            self.logger.info(f"SQL execution attempt {attempt_number}")

            # Validate SQL before execution
            if not validate_sql(final_sql):

                self.logger.error(
                    f"SQL validation failed on attempt " f"{attempt_number}"
                )

                return SQLResponse(
                    question=question,
                    sql=final_sql,
                    original_sql=original_sql,
                    answer="Generated SQL was unsafe or invalid.",
                    success=False,
                    was_fixed=was_fixed,
                    error="SQL validation failed.",
                )

            try:

                self.logger.info(f"Executing SQL on attempt " f"{attempt_number}")

                result = execute_sql(
                    db=self.db,
                    sql_query=final_sql,
                )

                self.logger.info(
                    f"SQL executed successfully on attempt " f"{attempt_number}"
                )

                # Stop retrying because execution succeeded
                break

            except Exception as e:

                last_error = str(e)

                self.logger.error(
                    f"SQL execution failed on attempt "
                    f"{attempt_number}: {last_error}"
                )

                # Check whether retry limit is reached
                if attempt == MAX_SQL_RETRIES:

                    self.logger.error("Maximum SQL retry limit reached")

                    return SQLResponse(
                        question=question,
                        sql=final_sql,
                        original_sql=original_sql,
                        answer=("SQL execution failed after " "multiple attempts."),
                        success=False,
                        was_fixed=was_fixed,
                        error=last_error,
                    )

                # Try fixing the SQL
                self.logger.info(
                    f"Attempting to fix SQL after " f"attempt {attempt_number}"
                )

                fixed_sql = fix_sql(
                    question=question,
                    schema=self.schema,
                    failed_sql=final_sql,
                    error=last_error,
                    llm=self.llm,
                )

                self.logger.info(f"Fixed SQL: {fixed_sql}")

                # Use fixed SQL for the next attempt
                final_sql = fixed_sql
                was_fixed = True

        # Generate final answer
        self.logger.info("Generating final answer")

        answer = generate_answer(
            question=question,
            sql=final_sql,
            result=result,
            llm=self.llm,
        )

        self.logger.info("Answer generated successfully")

        # Save successful conversation to memory
        self.memory.add(
            question=question,
            sql=final_sql,
            answer=answer,
        )

        self.logger.info("Conversation added to memory")

        return SQLResponse(
            question=question,
            sql=final_sql,
            original_sql=original_sql,
            answer=answer,
            success=True,
            was_fixed=was_fixed,
        )
