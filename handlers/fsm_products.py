from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from db import main_db


class FSMProduct(StatesGroup):
    name = State()
    category = State()
    size = State()
    price = State()
    product_id = State()
    photo = State()
    submit = State()

async def start_fsm_product(message: types.Message):
    await message.answer("Введите название товара:")
    await FSMProduct.name.set()


async def load_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text

    await FSMProduct.next()
    await message.answer("Введите категорию товара:")


async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text

    await FSMProduct.next()
    await message.answer("Введите размер товара:")


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await FSMProduct.next()
    await message.answer("Введите цену товара:")


async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text

    await FSMProduct.next()
    await message.answer("Введите артикул товара:")


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await FSMProduct.next()
    await message.answer("Отправьте фотографию товара:")


async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await FSMProduct.next()
    await message.answer(f'Верны ли данные?\n')
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название: {data["name"]}\n'
                                       f'Категория: {data["category"]}\n'
                                       f'Размер: {data["size"]}\n'
                                       f'Цена: {data["price"]}\n'
                                       f'Артикул: {data["product_id"]}\n')


async def load_submit(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            await main_db.sql_insert_product(
                name=data['name'],
                category=data['category'],
                size=data['size'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo'])
        await state.finish()
        await message.answer("Товар успешно добавлен!")
    elif message.text == 'Нет':
        await state.finish()
        await message.answer("Добавление товара отменено.")
    else:
        await message.answer("Некорректный ответ. Пожалуйста, отправьте 'Да' или 'Нет'.")


def fsm_product_handlers(dp: Dispatcher):
    dp.register_message_handler(start_fsm_product, commands=['product'])
    dp.register_message_handler(load_name, state=FSMProduct.name)
    dp.register_message_handler(load_category, state=FSMProduct.category)
    dp.register_message_handler(load_size, state=FSMProduct.size)
    dp.register_message_handler(load_price, state=FSMProduct.price)
    dp.register_message_handler(load_product_id, state=FSMProduct.product_id)
    dp.register_message_handler(load_photo, state=FSMProduct.photo, content_types=['photo'])
    dp.register_message_handler(load_submit, state=FSMProduct.submit)