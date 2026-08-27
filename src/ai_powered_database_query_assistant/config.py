import os

from dotenv import load_dotenv

load_dotenv()


DB_PATH = os.getenv("DB_PATH", "data/Chinook.db")

MODEL_NAME = os.getenv("MODEL_NAME", "openai/gpt-oss-120b")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.0"))

MAX_HISTORY = int(os.getenv("MAX_HISTORY", "5"))
