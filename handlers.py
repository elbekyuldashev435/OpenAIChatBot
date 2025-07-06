from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database import (add_user, set_language, get_language, count_last_minute_queries, save_query, get_all_users_with_queries)
from openai_api import get_openai_response
from utils import language_keyboard, get_text

router = Router()


@router.message(CommandStart())
async def start_cmd(msg: Message):
    await add_user(msg.from_user.id, msg.from_user.username)
    await msg.answer(get_text("welcome", "uz"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang_"))
async def lang_selected(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    await set_language(callback.from_user.id, lang)
    await callback.message.edit_text(get_text("enter_question", lang))


@router.message()
async def handle_question(msg: Message):
    lang = await get_language(msg.from_user.id)
    recent_count = await count_last_minute_queries(msg.from_user.id)
    if recent_count >= 3:
        await msg.answer(get_text("limit_exceeded", lang))
        return

    await msg.answer("⌛ Yuborilmoqda...")
    reply = await get_openai_response(msg.text)
    await save_query(msg.from_user.id, msg.text, reply)
    await msg.answer(reply)

    if msg.text.lower() in ["/users", "foydalanuvchilar", "пользователи"]:
        users_data = await get_all_users_with_queries()
        text = get_text("show_users", lang) + "\n\n"
        for uid, username, queries in users_data:
            text += f"👤 {username or uid}:\n"
            for q in queries:
                text += f"  — {q}\n"
            text += "\n"
        await msg.answer(text[:4096])
