import os
from dotenv import load_dotenv

load_dotenv(override=True)
GMAIL_FOLDER = os.getenv("GMAIL_FOLDER", "INBOX")
GMAIL_ADDRESS = os.environ["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = os.environ["GMAIL_APP_PASSWORD"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "granite4:3b")
OUTPUT_FOLDER = "output"