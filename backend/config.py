import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
DATA_DIR.mkdir(exist_ok=True)

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude")
LLM_CLAUDE_API_KEY = os.getenv("LLM_CLAUDE_API_KEY", "")
LLM_CLAUDE_MODEL = os.getenv("LLM_CLAUDE_MODEL", "claude-sonnet-4-6")
LLM_OPENAI_API_KEY = os.getenv("LLM_OPENAI_API_KEY", "")
LLM_OPENAI_MODEL = os.getenv("LLM_OPENAI_MODEL", "gpt-4o")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "phi3:mini")

SQLITE_PATH = os.getenv("SQLITE_PATH", str(DATA_DIR / "family_profiles.db"))
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "CHANGE_ME_TO_A_SECURE_32_BYTE_KEY!!")

CHROMA_PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIR", str(DATA_DIR / "chroma_store"))

CRAWL_SCHEDULE_DAY = os.getenv("CRAWL_SCHEDULE_DAY", "sun")
CRAWL_SCHEDULE_HOUR = int(os.getenv("CRAWL_SCHEDULE_HOUR", "3"))
CRAWL_SCHEDULE_MINUTE = int(os.getenv("CRAWL_SCHEDULE_MINUTE", "0"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
