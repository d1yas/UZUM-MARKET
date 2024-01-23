import logging
from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import CallbackQuery
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.default import keyboard
from keyboards.inline import Katalog1, Katalog2
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Core.settings')
application = get_wsgi_application()
# ------------------------DJANGO--------------------
from ProductAPP.views import filtr_by_katalog

API_TOKEN = '6029555538:AAGZVSM6OIOoomI92pIcy5Zm7tk4MtFR_Ys'
logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def startt(message: types.Message):
    await message.answer("Assalomu aleykum uzum marketga xush kelibiz! ", reply_markup=keyboard)


@dp.message_handler(text='Katalog')
async def katalog(message: types.Message):
    await message.answer('KATALOG', reply_markup=Katalog1)


@dp.callback_query_handler(text='oldinga')
async def oldinga_inline(call: types.CallbackQuery):
    try:
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=Katalog2)
    except:
        await call.answer('Boshqa menyu mavjud emas')


@dp.callback_query_handler(text='orqaga')
async def orqaga_inline(call: types.CallbackQuery):
    try:
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=Katalog1)
    except:
        await call.answer('Boshqa menyu mavjud emas')


from channels.db import database_sync_to_async


@dp.callback_query_handler()
async def catalog_oladi(call: types.CallbackQuery):
    print(call.data)
    # categorylar = filtr_by_katalog(call.data)
    # send callback data to django
    categorylar = await database_sync_to_async(filtr_by_katalog)(call.data)
    #get data from django



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
