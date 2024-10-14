import asyncio

import structlog
from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from api_client.variables import TELEGRAM_BOT_TOKEN
from handlers.start import start_handler
from handlers.notes import get_notes_handler
from utils.utils import set_commands

logger = structlog.get_logger(__name__)

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()


async def main():
    # handlers
    dp.message.register(start_handler, Command('start'))
    dp.message.register(get_notes_handler, Command('get_notes'))

    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logger.info('bot started')
    asyncio.run(main())
