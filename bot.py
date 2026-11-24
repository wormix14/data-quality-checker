import asyncio
import logging
from os import getenv

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from validator import validate_bronze, validate_gold, validate_silver
from dotenv import load_dotenv

load_dotenv(override=True)

dp = Dispatcher()

@dp.message(Command("start"))
async def send_welcome(message: Message):
    await message.reply("Bot started\nAvailable commands:\n<b>/bronze</b> - validate bronze taxi layer\n"
    "<b>/silver</b> - validate silver taxi layer\n"
    "<b>/gold</b> - validate gold taxi layer ", parse_mode="HTML")

@dp.message(Command("bronze"))
async def echo_bronze(message: Message):
    wait_msg = await message.answer("⏳ Validating Bronze layer...")
    response = await asyncio.to_thread(validate_bronze)
    await wait_msg.edit_text(response, parse_mode="HTML")

@dp.message(Command("silver"))
async def echo_silver(message: Message):
    wait_msg = await message.answer("⏳ Validating Silver layer...")
    response = await asyncio.to_thread(validate_silver)
    await wait_msg.edit_text(response, parse_mode="HTML")

@dp.message(Command("gold"))
async def echo_gold(message: Message):
    wait_msg = await message.answer("⏳ Validating Gold layer...")
    response = await asyncio.to_thread(validate_gold)
    await wait_msg.edit_text(response, parse_mode="HTML")
                            
async def main() -> None:
    bot = Bot(token=getenv("BOT_TOKEN"))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())