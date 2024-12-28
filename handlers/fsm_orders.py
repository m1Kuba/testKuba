from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from config import bot, Admins


class FSMOrder(StatesGroup):
    product_id = State()
    size = State()
    quantity = State()
    contact = State()


async def start_fsm_order(message: types.Message):
    await message.answer("Введите артикул товара:")
    await FSMOrder.product_id.set()


async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text

    await FSMOrder.next()
    await message.answer("Введите размер товара:")


async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text

    await FSMOrder.next()
    await message.answer("Введите количество товара:")


async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text

    await FSMOrder.next()
    await message.answer("Введите ваш номер телефона:")


async def load_contact(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contact'] = message.text

    order_details = (
        f"📦 Новый заказ:\n"
        f"Артикул: {data['product_id']}\n"
        f"Размер: {data['size']}\n"
        f"Количество: {data['quantity']}\n"
        f"Контакт: {data['contact']}\n"
    )

    for admin_id in Admins:
        try:
            await bot.send_message(admin_id, order_details)
        except Exception as e:
            print(f"Не удалось отправить сообщение администратору {admin_id}: {e}")

    await state.finish()
    await message.answer("Ваш заказ отправлен! С вами свяжутся в ближайшее время.")


def fsm_orders_handlers(dp: Dispatcher):
    dp.register_message_handler(start_fsm_order, commands=['order'])
    dp.register_message_handler(load_product_id, state=FSMOrder.product_id)
    dp.register_message_handler(load_size, state=FSMOrder.size)
    dp.register_message_handler(load_quantity, state=FSMOrder.quantity)
    dp.register_message_handler(load_contact, state=FSMOrder.contact)
