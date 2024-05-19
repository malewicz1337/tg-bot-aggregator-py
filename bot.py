import asyncio
import json
import logging
import os
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет! Отправь мне JSON с параметрами агрегации.")


@dp.message()
async def jsons_handler(message: Message) -> None:
    try:
        data = json.loads(message.text)
        dt_from = data["dt_from"]
        dt_upto = data["dt_upto"]
        group_type = data["group_type"]

        result = await aggregate_salaries(dt_from, dt_upto, group_type)
        response = json.dumps(result, indent=4, ensure_ascii=False)

        await message.reply(response)
    except Exception as e:
        await message.reply(f"Ошибка: {str(e)}")


async def main() -> None:
    bot = Bot(token=API_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
