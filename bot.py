import asyncio
import logging
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode

from api import GApiClient
from config import load_config
from handlers import router
from storage import UserStorage


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s"
)


HEARTBEAT_INTERVAL = 30
HEARTBEAT_MAX_FAILURES = 10


async def heartbeat(bot: Bot, dp: Dispatcher, path: str):
    file = Path(path)
    failures = 0

    while True:
        try:
            await bot.get_me()
            file.touch()
            failures = 0
        except Exception:
            failures += 1
            logging.exception("Heartbeat: Telegram недоступен")

            if failures >= HEARTBEAT_MAX_FAILURES:
                logging.critical("Heartbeat: нет связи с Telegram, перезапуск")
                await dp.stop_polling()
                return

        await asyncio.sleep(HEARTBEAT_INTERVAL)


async def main():
    config = load_config()

    session = (
        AiohttpSession(proxy=config.proxy)
        if config.proxy
        else AiohttpSession()
    )

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        ),
        session=session,
    )

    dp = Dispatcher()
    dp.include_router(router)

    storage = UserStorage(config.db_path)
    await storage.init()

    async with GApiClient(config.api_base_url) as api:
        dp["api"] = api
        dp["storage"] = storage

        await bot.delete_webhook(drop_pending_updates=True)

        heartbeat_task = asyncio.create_task(
            heartbeat(bot, dp, config.heartbeat_path)
        )

        try:
            await dp.start_polling(bot)
        finally:
            heartbeat_task.cancel()

        if heartbeat_task.done() and not heartbeat_task.cancelled():
            raise SystemExit(1)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
