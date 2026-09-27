from __future__ import annotations

import aiosqlite


class UserStorage:
    def __init__(self, db_path: str):
        self._db_path = db_path

    async def init(self):
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    group_name TEXT
                )
                """
            )
            await db.commit()

    async def set_group(self, user_id: int, group: str):
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute(
                """
                INSERT INTO users (user_id, group_name) VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET group_name = excluded.group_name
                """,
                (user_id, group),
            )
            await db.commit()

    async def get_group(self, user_id: int) -> str | None:
        async with aiosqlite.connect(self._db_path) as db:
            async with db.execute(
                "SELECT group_name FROM users WHERE user_id = ?", (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                return row[0] if row else None

    async def clear_group(self, user_id: int):
        async with aiosqlite.connect(self._db_path) as db:
            await db.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
            await db.commit()
