import asyncio
import logging
import os

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


async def main():
    config = load_config()

    proxy = os.getenv("PROXY", "").strip()
    if proxy:
        session = AiohttpSession(proxy=proxy)
        logging.getLogger(__name__).info("Используется прокси: %s", proxy)
    else:
        session = None

    bot = Bot(
        token=config.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
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
        await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
