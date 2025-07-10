import asyncio
import openai
from conf import OPENAI_API_KEY

if not OPENAI_API_KEY:
    raise ValueError("❌ OPENAI_API_KEY topilmadi")

openai.api_key = OPENAI_API_KEY
openai.api_base = "https://openrouter.ai/api/v1"
MODEL_NAME = "openai/gpt-4o"


async def get_openai_response(prompt: str) -> list[str]:
    try:
        lower_prompt = prompt.lower()

        if any(word in lower_prompt for word in ["islam", "din", "namoz", "qur'on", "halol", "harom", "ramazon", "duo"]):
            system_content = (
                "You are an expert in Islamic teachings and world religions. "
                "Always interpret religious-related questions correctly. "
                "Answer briefly, respectfully, and accurately without adding unrelated information."
            )
        elif any(word in lower_prompt for word in ["python", "code", "program", "html", "django", "api", "bot", "backend", "frontend"]):
            system_content = (
                "You are a senior software engineer and expert in AI technologies. "
                "Answer technical questions clearly, with examples when necessary, and keep the response concise."
            )
        elif any(word in lower_prompt for word in ["science", "biology", "mathematics", "physics", "school", "education"]):
            system_content = (
                "You are a knowledgeable teacher and education assistant. "
                "Provide well-structured, factual, and understandable answers to questions about science, technology, and education."
            )
        elif any(word in lower_prompt for word in ["translate", "tarjima", "ingliz", "rus", "uzbek", "til", "language"]):
            system_content = (
                "You are a language expert and professional translator. "
                "Help users translate, understand, or learn different languages, especially between English, Russian, and Uzbek. "
                "Avoid misinterpreting cultural phrases or idioms."
            )
        else:
            system_content = (
                "You are a helpful and polite assistant who answers questions accurately and clearly. "
                "Always provide useful, relevant, and respectful answers."
            )

        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: openai.ChatCompletion.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1400,
            temperature=0.7
        ))

        full_text = response.choices[0].message["content"].strip()
        max_len = 4096
        return [full_text[i:i+max_len] for i in range(0, len(full_text), max_len)]

    except Exception as e:
        return [f"❌ Xatolik yuz berdi: {e}"]