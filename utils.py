from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])

def get_text(key: str, lang: str) -> str:
    texts = {
        "welcome": {
            "uz": "Assalomu alaykum! Tilni tanlang:",
            "ru": "Здравствуйте! Пожалуйста, выберите язык:",
            "en": "Hello! Please select your language:"
        },
        "enter_question": {
            "uz": "Qanday mavzuda savolingiz bor?",
            "ru": "На какую тему у вас вопрос?",
            "en": "What is your question about?"
        },
        "limit_exceeded": {
            "uz": "❌ Siz 1 daqiqada 3 ta so‘rov yubordingiz. Iltimos, keyinroq urinib ko‘ring.",
            "ru": "❌ Вы отправили 3 запроса за минуту. Попробуйте позже.",
            "en": "❌ You've sent 3 requests in 1 minute. Try again later."
        },
        "show_users": {
            "uz": "📋 Foydalanuvchilar ro'yxati:",
            "ru": "📋 Список пользователей:",
            "en": "📋 User list:"
        }
    }
    return texts.get(key, {}).get(lang, "")
