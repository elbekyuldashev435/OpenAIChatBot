# 📡 Telegram Chatbot (Multi-language)

Bu loyiha – Python yordamida yaratilgan, SQLite ma'lumotlar bazasidan foydalanadigan, uch tilda (O'zbek, Rus, Ingliz) ishlovchi Telegram bot. Foydalanuvchilar savollar berishi va botdan tezkor javoblar olishi mumkin. OpenAI API ishlatilmagan.

## 🔧 Texnologiyalar
- Python 3.11+
- aiogram 3.x
- SQLite3
- dotenv (maxfiy ma’lumotlar uchun)
- asyncio

## 🚀 Xususiyatlar
- ✅ OpenAI ishlatilmagan (kompaniya talabi asosida)
- ✅ Daqiqasiga 3 so‘rov bilan cheklangan
- ✅ Har bir foydalanuvchining so‘rov soni va oxirgi so‘rov vaqti log qilinadi
- ✅ Oddiy va tushunarli interfeys
- ✅ Foydalanuvchi tili bo‘yicha mos javob (uz/ru/en)
- ✅ Admin panel (buyruqlar orqali)
- ✅ Foydalanuvchilar ro‘yxatini ko‘rish imkoniyati

## 🗂 Papkalar tuzilmasi

chatbot_project/
├── handlers/ # Bot handlerlari
├── database/ # SQLite bilan ishlovchi fayllar
├── middlewares/ # So‘rov cheklovchi middleware
├── messages/ # Har xil tillardagi javoblar
├── .env.txt # Maxfiy sozlamalar
├── main.py # Botni ishga tushiruvchi fayl
└── requirements.txt # Loyihaga kerakli kutubxonalar


## 🔑 .env fayl namunasi
`.env.txt` fayliga quyidagilarni yozing:

BOT_TOKEN=your_telegram_bot_token_here
ADMINS=123456789 # Admin Telegram ID


## 💻 Ishga tushirish

```bash
# virtual muhit yaratish (ixtiyoriy)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# talablar o‘rnatiladi
pip install -r requirements.txt

# botni ishga tushirish
python main.py


👨‍💻 Muallif
Ismi: Elbek Yuldashev

Telegram: elbek_prgm
