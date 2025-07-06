import openai
from conf import OPENAI_API_KEY


openai.api_key = OPENAI_API_KEY


async def get_openai_response(prompt: str) -> str:
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"❌ OpenAI xatolik berdi: {e}"
