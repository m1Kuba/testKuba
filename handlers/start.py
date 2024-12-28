from aiogram import types, Dispatcher
from config import bot

async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Добро пожаловать, {message.from_user.first_name}!\n\n'
                                'я бот для работы с товарами.\n'
                           'для более подробной информации напишите /info')

async def info_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text="Привет!\n"
                                "Я бот, который помогает управлять товарами и заказами:\n"
                                "- Сотрудники могут добавлять и редактировать товары.\n"
                                "- Клиенты могут просматривать товары и оформлять заказы.\n\n")

def start_register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=['start'])
    dp.register_message_handler(info_handler, commands=['info'])