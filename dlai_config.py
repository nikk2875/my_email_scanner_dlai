import os
from dotenv import load_dotenv

load_dotenv(override=True)

# Define input/output
GMAIL_FOLDER = os.getenv("GMAIL_FOLDER", "INBOX")
GMAIL_ADDRESS = os.getenv("GMAIL_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")
OUTPUT_FOLDER = "output"

# Define providers URL
ANTHROPIC_BASE_URL = "https://api.anthropic.com/v1/"
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"
GROK_BASE_URL = "https://api.x.ai/v1"
GROQ_BASE_URL = "https://api.groq.com/openai/v1"
OLLAMA_BASE_URL = "http://localhost:11434/v1"

# Set API keys
openai_api_key = os.getenv('OPENAI_API_KEY')
anthropic_api_key = os.getenv('ANTHROPIC_API_KEY')
gemini_api_key = os.getenv('GOOGLE_API_KEY')
grok_api_key = os.getenv('GROK_API_KEY')
groq_api_key = os.getenv('GROQ_API_KEY')

# Define models
OPENAI_MODEL = "gpt-5.4"
ANTHROPIC_MODEL = "claude-haiku-4-5-20251001"
GEMINI_MODEL = "gemini-3.1-flash-lite-preview"
GROK_MODEL = "grok-4.20-0309-reasoning"
GROQ_MODEL = "llama-3.3-70b-versatile"
OLLAMA_MODEL = "phi4:14b"