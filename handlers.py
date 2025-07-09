from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from database import (add_user, set_language, get_language, count_last_minute_queries, save_query, get_all_users_with_queries)
from openai_api import get_openai_response
from utils import language_keyboard, get_text
import os
from dotenv import load_dotenv
from database import get_users_with_query_stats
from aiogram.types import FSInputFile
import csv

router = Router()

load_dotenv('.env.txt')

ADMIN_ID = int(os.getenv("ADMIN_ID"))


@router.message()
async def handle_question(msg: Message):
    lang = await get_language(msg.from_user.id)

    text_lower = msg.text.lower()

    if text_lower in ["/users", "/foydalanuvchilar", "/пользователи"]:
        if msg.from_user.id == ADMIN_ID:
            users_data = await get_users_with_query_stats()
            text = "📋 Foydalanuvchilar ro'yxati:\n\n"
            csv_rows = [("ID", "Username", "So‘rovlar soni", "So‘nggi so‘rov")]

            for uid, username, count, last_query in users_data:
                display_name = username or str(uid)
                text += f"👤 {display_name}:\n"
                text += f"  — So‘rovlar soni: {count}\n"
                text += f"  — Oxirgi so‘rov: {last_query or 'Yo‘q'}\n\n"
                csv_rows.append((uid, username or "", count, last_query or "Yo‘q"))

            await msg.answer(text[:4096])

            with open("users_export.csv", "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(csv_rows)

            file = FSInputFile("users_export.csv")
            await msg.answer_document(file, caption="📄 Foydalanuvchilar statistikasi (CSV)")

            os.remove("users_export.csv")
        else:
            await msg.answer("❌ Bu buyruq faqat admin uchun.")
        return

    if msg.from_user.id != ADMIN_ID:
        recent_count = await count_last_minute_queries(msg.from_user.id)
        if recent_count >= 3:
            await msg.answer(get_text("limit_exceeded", lang))
            return

    await msg.answer("⌛ Yuborilmoqda...")
    reply = await get_openai_response(msg.text)
    await save_query(msg.from_user.id, msg.text, reply)
    await msg.answer(reply)


@router.message(CommandStart())
async def start_cmd(msg: Message):
    await add_user(msg.from_user.id, msg.from_user.username)
    await msg.answer(get_text("welcome", "uz"), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang_"))
async def lang_selected(callback: CallbackQuery):
    lang = callback.data.split("_")[1]
    await set_language(callback.from_user.id, lang)
    await callback.message.edit_text(get_text("enter_question", lang))