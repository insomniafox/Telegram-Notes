import os

import asyncio

import httpx
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()
client = httpx.AsyncClient(verify=False)


@dp.message(Command('start'))
async def start_handler(message: Message, command: CommandObject):
    token = command.args
    user_id = message.from_user.id
    url = 'http://localhost:8010/api/telegram/set_telegram_id'
    data = {
        "token": token,
        "telegram_id": user_id
    }
    response = await client.post(url=url, json=data)
    print(response)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
