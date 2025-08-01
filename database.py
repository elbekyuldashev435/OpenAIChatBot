import aiosqlite
from datetime import datetime, timedelta
import sqlite3


DB_NAME = 'bot_db.sqlite'


async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                language TEXT,
                joined_at TEXT
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS queries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                prompt TEXT,
                response TEXT,
                asked_at TEXT
            )
        """)
        await db.commit()


async def add_user(user_id, username):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "INSERT OR REPLACE INTO users (user_id, username, joined_at) VALUES (?, ?, ?)",
            (user_id, username, datetime.now().isoformat())
        )
        await db.commit()


async def set_language(user_id, lang):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE users SET language = ? WHERE user_id = ?",
            (lang, user_id)
        )
        await db.commit()


async def get_language(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute(
            "SELECT language FROM users WHERE user_id = ?", (user_id,)
        ) as cursor:
            row = await cursor.fetchone()
            return row[0] if row else "uz"


async def count_queries(user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT COUNT(*) FROM queries
            WHERE user_id = ? AND date(asked_at) = date('now')
        """, (user_id,)) as cursor:
            row = await cursor.fetchone()
            return row[0]


async def save_query(user_id, prompt, response):
    if isinstance(response, list):
        response = "\n\n".join(response)

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("""
            INSERT INTO queries (user_id, prompt, response, asked_at)
            VALUES (?, ?, ?, ?)
        """, (user_id, prompt, response, datetime.now().isoformat()))
        await db.commit()


async def get_all_users_with_queries():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT user_id, username FROM users") as cursor:
            users = await cursor.fetchall()
        result = []
        for user_id, username in users:
            async with db.execute("""
                SELECT prompt FROM queries
                WHERE user_id = ?
            """, (user_id,)) as q_cursor:
                queries = await q_cursor.fetchall()
                result.append((user_id, username, [q[0] for q in queries]))
        return result


async def count_last_minute_queries(user_id):
    one_minute_ago = datetime.now() - timedelta(seconds=60)
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT COUNT(*) FROM queries
            WHERE user_id = ? AND asked_at >= ?
        """, (user_id, one_minute_ago.isoformat())) as cursor:
            row = await cursor.fetchone()
            return row[0]


async def get_users_with_query_stats():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("""
            SELECT u.user_id, u.username, COUNT(q.id), MAX(q.asked_at)
            FROM users u
            LEFT JOIN queries q ON u.user_id = q.user_id
            GROUP BY u.user_id
            ORDER BY MAX(q.asked_at) DESC
        """) as cursor:
            rows = await cursor.fetchall()

    results = []
    for user_id, username, count, last_time in rows:
        if last_time:
            try:
                formatted_time = datetime.fromisoformat(last_time).strftime("%Y-%m-%d %H:%M:%S")
            except:
                formatted_time = last_time
        else:
            formatted_time = "So‘rov yo‘q"
        results.append((user_id, username, count, formatted_time))

    return results