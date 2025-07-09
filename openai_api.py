import openai
from conf import OPENAI_API_KEY

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY topilmadi. Iltimos .env.txt faylni tekshiring.")

openai.api_key = OPENAI_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"
MODEL_NAME = "openai/gpt-4o"


async def get_openai_response(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message["content"].strip()
    except Exception as e:
        return f"❌ Xatolik yuz berdi: {e}"