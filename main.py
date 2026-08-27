from dotenv import load_dotenv

from src.database import get_database
from src.schema import get_schema
from src.llm import get_llm
from src.sql_generator import generate_sql
from src.validator import validate_sql
from src.executor import execute_sql
from src.sql_fixer import fix_sql
from src.answer_generator import generate_answer

load_dotenv()


# Database
db = get_database("data/Chinook.db")

# Schema
schema = get_schema(db)

# LLM
llm = get_llm()


# User question
question = "Show the top 5 customers by total spending."


# Generate SQL
sql = generate_sql(question=question, schema=schema, llm=llm)

print(f"\nQuestion:\n{question}")
print(f"\nGenerated SQL:\n{sql}")


# Store the final SQL
final_sql = None
result = None


# Validate generated SQL
if not validate_sql(sql):

    print("\nGenerated unsafe or invalid SQL.")

else:

    try:
        # First execution attempt
        result = execute_sql(db=db, sql_query=sql)

        final_sql = sql

    except Exception as e:

        print("\nInitial SQL failed. Trying to fix it...")

        error = str(e)

        # Fix SQL
        fixed_sql = fix_sql(
            question=question, schema=schema, failed_sql=sql, error=error, llm=llm
        )

        print(f"\nFixed SQL:\n{fixed_sql}")

        # Validate fixed SQL
        if validate_sql(fixed_sql):

            try:
                result = execute_sql(db=db, sql_query=fixed_sql)

                final_sql = fixed_sql

            except Exception as e:
                print(f"\nFixed SQL also failed:\n{e}")

        else:
            print("\nFixed SQL is unsafe or invalid.")


# Generate final answer
if result is not None:

    answer = generate_answer(question=question, sql=final_sql, result=result, llm=llm)

    print(f"\nAnswer:\n{answer}")
