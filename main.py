import logging
from aiogram import executor
from config import dp, bot, Admins
from handlers import start, fsm_products, products, fsm_orders
from db import main_db

async def on_startup(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот включен!')
    await main_db.create_db()


start.start_register_handlers(dp)
fsm_products.fsm_product_handlers(dp)
products.register_handlers_products(dp)
fsm_orders.fsm_orders_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
