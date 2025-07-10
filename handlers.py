from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database import (
    add_user, set_language, get_language,
    count_last_minute_queries, save_query,
    get_users_with_query_stats, get_all_users_with_queries
)
from openai_api import get_openai_response
from utils import language_keyboard, get_text
import os
from dotenv import load_dotenv
from datetime import datetime
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

load_dotenv('.env.txt')

ADMIN_ID = int(os.getenv("ADMIN_ID"))

TEXTS = {
    "welcome": {
        "uz": """
👋 Assalomu alaykum!

Men OpenAI asosidagi sun’iy intellekt chatbotman 🤖.
Quyidagicha savollarga javob bera olaman:

🕌 Diniy savollar (Islom, Qur'on, ibodatlar)
💻 Dasturlash va texnika (Python, Django, botlar)
🎓 Fan va ta'lim (matematika, fizika, biologiya)
🌐 Til o‘rganish va tarjima (uz/ru/en)
🔍 Oddiy hayotiy savollar

❗ Har daqiqada 3 ta so‘rov yuborish mumkin.

Savolingizni yozing va javobni kuting ⌛
""",
        "ru": """
👋 Привет!

Я — интеллектуальный чат-бот на базе OpenAI 🤖.
Я могу помочь вам с:

🕌 Вопросами о религии (Ислам, Коран, намаз)
💻 Программированием и технологиями (Python, Django, боты)
🎓 Наукой и образованием (математика, физика, биология)
🌐 Переводами и языками (уз/ру/англ)
🔍 Обычными жизненными вопросами

❗ Можно отправить до 3 запросов в минуту.

Напишите вопрос и дождитесь ответа ⌛
""",
        "en": """
👋 Hello!

I'm an AI chatbot powered by OpenAI 🤖.
I can help you with:

🕌 Religious questions (Islam, Qur'an, prayers)
💻 Programming and tech (Python, Django, bots)
🎓 Science and education (math, physics, biology)
🌐 Translation and language (uz/ru/en)
🔍 Everyday questions

❗ You can ask up to 3 questions per minute.

Type your question and wait for the answer ⌛
"""
    }
}

def get_welcome_text(key: str, lang: str = "uz") -> str:
    return TEXTS.get(key, {}).get(lang, "❌ Matn topilmadi.")


@router.callback_query()
async def language_selected(callback: CallbackQuery):
    lang_code = callback.data
    user_id = callback.from_user.id

    await set_language(user_id, lang_code)

    welcome_message = get_welcome_text("welcome", lang_code)
    await callback.message.answer(welcome_message)

    await callback.answer()


def language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O'zbek", callback_data="uz"),
            InlineKeyboardButton(text="🇷🇺 Русский", callback_data="ru"),
            InlineKeyboardButton(text="🇬🇧 English", callback_data="en")
        ]
    ])


@router.message(CommandStart())
async def start_cmd(msg: Message):
    await add_user(msg.from_user.id, msg.from_user.username)
    await msg.answer("Iltimos, tilni tanlang:", reply_markup=language_keyboard())


@router.message(F.text.lower() == "/users")
async def list_users(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("❌ Bu buyruq faqat admin uchun.")
        return

    users_data = await get_users_with_query_stats()
    text = "📋 Foydalanuvchilar ro'yxati:\n\n"

    for uid, username, count, last_query in users_data:
        display_name = username or str(uid)
        if last_query:
            try:
                dt = datetime.fromisoformat(last_query)
                formatted_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = last_query
        else:
            formatted_time = "Yo‘q"

        text += f"👤 {display_name}:\n"
        text += f"  — So‘rovlar soni: {count}\n"
        text += f"  — Oxirgi so‘rov: {formatted_time}\n\n"

    await msg.answer(text[:4096])


@router.message(F.text.lower() == "/history")
async def show_history(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("❌ Bu buyruq faqat admin uchun.")
        return

    users_queries = await get_all_users_with_queries()
    for user_id, username, prompts in users_queries:
        name = username or str(user_id)
        text = f"🧾 {name} so'rovlari ({len(prompts)} ta):\n"
        for i, p in enumerate(prompts, start=1):
            text += f"{i}. {p[:50]}...\n"
        await msg.answer(text[:4096])


@router.message(F.text.lower() == "/top")
async def top_users(msg: Message):
    if msg.from_user.id != ADMIN_ID:
        await msg.answer("❌ Bu buyruq faqat admin uchun.")
        return

    stats = await get_users_with_query_stats()
    sorted_stats = sorted(stats, key=lambda x: x[2], reverse=True)[:5]

    text = "🏆 Eng faol foydalanuvchilar:\n\n"
    for i, (user_id, username, count, last_time) in enumerate(sorted_stats, start=1):
        display = username or str(user_id)
        text += f"{i}. {display} — {count} so‘rov\n"

    await msg.answer(text)


@router.message()
async def handle_question(msg: Message):
    user_id = msg.from_user.id
    lang = await get_language(user_id)

    if user_id != ADMIN_ID:
        query_count = await count_last_minute_queries(user_id)
        if query_count >= 3:
            await msg.answer(get_text("limit_exceeded", lang))
            return

    await msg.answer("⌛ Yuborilmoqda...")
    reply_parts = await get_openai_response(msg.text)

    for part in reply_parts:
        await msg.answer(part)

    await save_query(user_id, msg.text, reply_parts)