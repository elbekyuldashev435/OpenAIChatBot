import os
from dotenv import load_dotenv

if os.getenv("RAILWAY_ENVIRONMENT"):
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
else:
    load_dotenv(".env.txt")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
