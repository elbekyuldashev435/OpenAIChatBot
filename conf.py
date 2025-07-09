import os
from dotenv import load_dotenv

if not os.getenv("RAILWAY_ENVIRONMENT"):
    load_dotenv('.env.txt')

BOT_TOKEN = os.environ.get("BOT_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))

print("OPENAI_API_KEY:", OPENAI_API_KEY)