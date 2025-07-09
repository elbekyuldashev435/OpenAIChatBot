import os
from dotenv import load_dotenv


if not os.getenv("RAILWAY_ENVIRONMENT"):
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")