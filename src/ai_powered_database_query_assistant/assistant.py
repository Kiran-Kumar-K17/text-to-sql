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


class SQLAssistant:

    def __init__(self, db: SQLDatabase, llm: BaseChatModel):
        self.db = db
        self.llm = llm
        self.schema = get_schema(db)
        self.memory = ConversationMemory()
        self.logger = get_logger(__name__)

    def ask(self, question: str) -> dict:

        self.logger.info(f"Received question: {question}")

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
        context = self.memory.get_context()

        self.logger.info("Generating SQL")
        # Generate SQL
        sql = generate_sql(
            question=question, schema=self.schema, llm=self.llm, context=context
        )
        self.logger.info(f"Generated SQL: {sql}")
        original_sql = sql
        was_fixed = False

        # Validate SQL
        if not validate_sql(sql):
            self.logger.warning("Generated SQL failed validation")
            return SQLResponse(
                question=question,
                sql=sql,
                answer="Generated SQL was unsafe or invalid.",
                success=False,
                error="SQL validation failed.",
            )

        final_sql = sql
        result = None
        self.logger.info("SQL validation passed")
        try:
            self.logger.info("Executing SQL")
            # First execution attempt
            result = execute_sql(db=self.db, sql_query=sql)
            self.logger.info("SQL executed successfully")

        except Exception as e:
            self.logger.error(f"SQL execution failed: {e}")

            self.logger.info("Attempting to fix SQL")
            # Try fixing SQL
            fixed_sql = fix_sql(
                question=question,
                schema=self.schema,
                failed_sql=sql,
                error=str(e),
                llm=self.llm,
            )
            self.logger.info(f"Fixed SQL: {fixed_sql}")

            # Validate fixed SQL
            if not validate_sql(fixed_sql):
                self.logger.error("Fixed SQL failed validation")
                return SQLResponse(
                    question=question,
                    sql=fixed_sql,
                    original_sql=original_sql,
                    answer="The generated SQL could not be safely fixed.",
                    success=False,
                    was_fixed=True,
                    error="Fixed SQL validation failed.",
                )

            try:
                self.logger.info("Executing fixed SQL")
                # Execute fixed SQL
                result = execute_sql(db=self.db, sql_query=fixed_sql)
                self.logger.info("Fixed SQL executed successfully")

                final_sql = fixed_sql
                was_fixed = True
            except Exception as e:
                self.logger.error(f"Fixed SQL execution failed: {e}")
                return SQLResponse(
                    question=question,
                    sql=fixed_sql,
                    answer="SQL execution failed.",
                    success=False,
                    error=str(e),
                )
        self.logger.info("Generating final answer")
        # Generate natural language answer
        answer = generate_answer(
            question=question, sql=final_sql, result=result, llm=self.llm
        )
        self.logger.info("Answer generated successfully")
        # Add to conversation memory
        self.memory.add(question=question, sql=final_sql, answer=answer)
        self.logger.info("Conversation added to memory")
        return SQLResponse(
            question=question,
            sql=final_sql,
            original_sql=original_sql,
            answer=answer,
            success=True,
            was_fixed=was_fixed,
        )
