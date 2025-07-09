from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="lang_uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_en")]
    ])


texts = {
    "uz": {
        "welcome": "Assalomu alaykum! Tilni tanlang:",
        "enter_question": "Qanday mavzuda savolingiz bor?",
        "limit_exceeded": "❌ Siz 1 daqiqada 3 ta so‘rov yubordingiz. Iltimos, keyinroq urinib ko‘ring.",
        "show_users": "📋 Foydalanuvchilar ro'yxati:",
        "admin_only": "❌ Bu buyruq faqat admin uchun.",
        "sending": "⌛ Yuborilmoqda..."
    },
    "ru": {
        "welcome": "Здравствуйте! Пожалуйста, выберите язык:",
        "enter_question": "На какую тему у вас вопрос?",
        "limit_exceeded": "❌ Вы отправили 3 запроса за минуту. Попробуйте позже.",
        "show_users": "📋 Список пользователей:",
        "admin_only": "❌ Эта команда доступна только администратору.",
        "sending": "⌛ Отправляется..."
    },
    "en": {
        "welcome": "Hello! Please select your language:",
        "enter_question": "What is your question about?",
        "limit_exceeded": "❌ You've sent 3 requests in 1 minute. Try again later.",
        "show_users": "📋 User list:",
        "admin_only": "❌ This command is only for the admin.",
        "sending": "⌛ Sending..."
    }
}


def get_text(key: str, lang: str) -> str:
    return texts.get(lang, texts["uz"]).get(key, "❌ Matn topilmadi.")
