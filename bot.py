import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import TOKEN_API
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.webhook import SendMessage
from aiogram.utils.executor import start_webhook
from commands import HELP_COMMANDS, DESCRIPTION


WEBHOOK_HOST = 'https://firstcontainer-rrjws.run-eu-central1.goorm.site'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = 8000

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot)
dp.middleware.setup (LoggingMiddleware())


kb = InlineKeyboardMarkup() # !!!
b1 = InlineKeyboardButton(text='Котики',
                          url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
b2 = InlineKeyboardButton(text='Собачки',
                          url='https://www.youtube.com/watch?v=dQw4w9WgXcQ')
kb.add(b1, b2)

@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id, text=HELP_COMMANDS)
    await message.reply('Информация была отправлена в личные сообщения')

@dp.message_handler(commands=['description'])
async def description(message: types.Message):
    await message.answer(text=DESCRIPTION)
    await message.delete()

@dp.message_handler(commands=['voting'])
async def voting(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Сделай свой выбор!',
                           reply_markup=kb)

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)



async def on_shutdown(dp):
    logging.warning ('Shutting down..')
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning ('Bye!')


if __name__ == '__main__':
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
)
