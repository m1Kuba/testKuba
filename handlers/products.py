from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import main_db

async def send_all_products(call: types.CallbackQuery):
    products = main_db.fetch_all_products()

    if products:
        for product in products:
            caption = (f"Название: {product['name']}\n"
                      f"Категория: {product['category']}\n"
                      f"Размер: {product['size']}\n"
                      f"Цена: {product['price']}\n"
                      f"Артикул: {product['product_id']}")

            await call.message.answer_photo(photo=product['photo'], caption=caption)
    else:
        await call.message.answer("Товары не найдены.")


def register_handlers_products(dp: Dispatcher):
    dp.register_callback_query_handler(send_all_products, Text(equals='products'))