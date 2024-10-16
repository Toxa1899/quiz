import asyncio
import logging
import sys
from os import getenv

from aiogram import Bot, Dispatcher, html, types
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, Message,
                           WebAppInfo)
from aiogram.utils.keyboard import InlineKeyboardBuilder

# Bot token can be obtained via https://t.me/BotFather
TOKEN = "6625369761:AAE1TKu6tVr3eg6qQjDLWQBFCpGEz-1CGyM"

# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()

def ease_link_kb():
    inline_kb_list = [
        [InlineKeyboardButton(text="Нажми меня", url='https://habr.com/ru/users/yakvenalex/')],

    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_kb_list)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    print(message.from_user.first_name)
    print(message.from_user.id)
    await message.answer( "Нажмите на кнопку, чтобы авторизоваться", reply_markup=ease_link_kb())

@dp.message()
async def echo_handler(message: Message) -> None:
    await message.answer('для авторизации нажмите /start ')

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())