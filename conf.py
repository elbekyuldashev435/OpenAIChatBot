import os
from dotenv import load_dotenv

if not os.getenv("RAILWAY_ENVIRONMENT"):
    load_dotenv('.env.txt')

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not os.getenv("RAILWAY_ENVIRONMENT"):
    print("BOT_TOKEN:", BOT_TOKEN)
    print("OPENAI_API_KEY:", OPENAI_API_KEY)