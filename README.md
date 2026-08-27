# AI-Powered Database Query Assistant

An AI-powered **Text-to-SQL assistant** that converts natural-language questions into SQL, safely validates and executes them, automatically fixes failed SQL, and returns a human-readable answer.

## Features

- Natural language to SQL
- Question validation
- SQL safety validation
- Read-only SQL protection
- SQL execution
- Automatic SQL fixing and retries
- Conversation memory
- Logging
- Unit and integration tests
- 98% test coverage

## Project Flow

```text
User Question
      ↓
Question Validation
      ↓
SQL Generation
      ↓
SQL Safety Validation
      ↓
SQL Execution
      ├── Success → Generate Final Answer
      └── Failure → Fix SQL → Retry
```

## Project Structure

```text
text-to-sql/
├── main.py
├── pyproject.toml
├── README.md
├── src/
│   └── ai_powered_database_query_assistant/
│       ├── assistant.py
│       ├── answer_generator.py
│       ├── config.py
│       ├── database.py
│       ├── executor.py
│       ├── llm.py
│       ├── logger.py
│       ├── memory.py
│       ├── models.py
│       ├── question_validator.py
│       ├── schema.py
│       ├── sql_fixer.py
│       ├── sql_generator.py
│       └── validator.py
├── test/
│   ├── test_assistant.py
│   ├── test_executor.py
│   ├── test_integration.py
│   ├── test_memory.py
│   ├── test_sql_fixer.py
│   └── test_validator.py
└── notebooks/
    └── text_to_sql.ipynb
```

## Installation

```bash
git clone https://github.com/Kiran-Kumar-K17/text-to-sql.git
cd text-to-sql
uv sync
```

## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

## Running

```bash
uv run python main.py
```

Example:

```text
How many customers are there?
```

## Testing

Run all tests:

```bash
uv run pytest -v
```

Current result:

```text
26 passed
```

Run coverage:

```bash
uv run pytest --cov=ai_powered_database_query_assistant --cov-report=term-missing
```

Current overall coverage:

```text
98%
```

## Code Quality

Check code with Ruff:

```bash
uv run ruff check .
```

Automatically fix supported issues:

```bash
uv run ruff check . --fix
```

## SQL Safety

The assistant allows read-only SQL such as:

```sql
SELECT * FROM Customer
```

```sql
WITH customer_data AS (
    SELECT * FROM Customer
)
SELECT * FROM customer_data
```

It blocks potentially dangerous operations including:

```text
DELETE
UPDATE
DROP
PRAGMA
ATTACH
```

Multiple SQL statements are also rejected.

## Retry Logic

```text
Attempt 1
   ↓
Execution fails
   ↓
Fix SQL
   ↓
Retry
   ↓
Success → Generate answer

OR

Maximum retries reached → Controlled failure response
```

## Tech Stack

- Python
- LangChain
- Groq
- SQLite
- pytest
- pytest-cov
- Ruff
- uv

## Future Improvements

- Streamlit or FastAPI frontend
- Multiple database support
- Query history
- Streaming responses
- Docker support
- GitHub Actions CI/CD
- Additional integration tests

## License

Currently created for learning and portfolio purposes.
