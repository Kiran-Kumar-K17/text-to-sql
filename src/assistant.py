from langchain_community.utilities import SQLDatabase
from langchain_core.language_models import BaseChatModel

from src.schema import get_schema
from src.sql_generator import generate_sql
from src.validator import validate_sql
from src.executor import execute_sql
from src.sql_fixer import fix_sql
from src.answer_generator import generate_answer
from src.models import SQLResponse


class SQLAssistant:

    def __init__(self, db: SQLDatabase, llm: BaseChatModel):
        self.db = db
        self.llm = llm
        self.schema = get_schema(db)

    def ask(self, question: str) -> dict:

        # Generate SQL
        sql = generate_sql(question=question, schema=self.schema, llm=self.llm)

        # Validate SQL
        if not validate_sql(sql):
            return SQLResponse(
                question=question,
                sql=sql,
                answer="Generated SQL was unsafe or invalid.",
                success=False,
                error="SQL validation failed.",
            )

        final_sql = sql
        result = None

        try:
            # First execution attempt
            result = execute_sql(db=self.db, sql_query=sql)

        except Exception as e:

            # Try fixing SQL
            fixed_sql = fix_sql(
                question=question,
                schema=self.schema,
                failed_sql=sql,
                error=str(e),
                llm=self.llm,
            )

            # Validate fixed SQL
            if not validate_sql(fixed_sql):
                return SQLResponse(
                    question=question,
                    sql=fixed_sql,
                    answer="The generated SQL could not be safely fixed.",
                    success=False,
                    error="Fixed SQL validation failed.",
                )

            try:
                # Execute fixed SQL
                result = execute_sql(db=self.db, sql_query=fixed_sql)

                final_sql = fixed_sql

            except Exception as e:
                return SQLResponse(
                    question=question,
                    sql=fixed_sql,
                    answer="SQL execution failed.",
                    success=False,
                    error=str(e),
                )

        # Generate natural language answer
        answer = generate_answer(
            question=question, sql=final_sql, result=result, llm=self.llm
        )

        return SQLResponse(
            question=question, sql=final_sql, answer=answer, success=True
        )
