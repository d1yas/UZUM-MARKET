import logging
from aiogram.types import ReplyKeyboardRemove
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from keyboards.default import keyboard
from keyboards.inline import Katalog1, Katalog2
from states import CallbackStates
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
# ------------------------DATABASE--------------------
from aiogram.dispatcher import FSMContext
import sqlite3
from aiogram.types import InputMedia

connect = sqlite3.connect('../db.sqlite3', check_same_thread=False)
cursor = connect.cursor()
from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
API_TOKEN = env.str('API_TOKEN')  # Bot token
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili

# ------------------------DATABASE--------------------

# API_TOKEN = "6586939529:AAF8J4lGLyO0LSCmpKHnBj14OkuvwgD76jc"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands="start")
async def startt(message: types.Message):
    await message.answer("Assalomu aleykum uzum marketga xush kelibiz! ", reply_markup=keyboard)


@dp.message_handler(text='Katalog')
async def katalog(message: types.Message):
    await message.answer('Kataloglardan Birini tanlang', reply_markup=ReplyKeyboardRemove())
    await message.answer('KATALOG', reply_markup=Katalog1)
    await CallbackStates.chala.set()


@dp.callback_query_handler(text='edit_orqa', state=CallbackStates.chala)
async def orqaga_inline(call: types.CallbackQuery):
    try:
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=Katalog1)
    except:
        await call.answer('Boshqa menyu mavjud emas')


@dp.callback_query_handler(text='edit_oldin', state=CallbackStates.chala)
async def oldinga_inline(call: types.CallbackQuery):
    try:
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=Katalog2)
    except:
        await call.answer('Boshqa menyu mavjud emas')


@dp.callback_query_handler(state=CallbackStates.chala)
async def kiyimlar_handler(call: types.CallbackQuery):
    print('Chala ishladi')
    try:
        categorylar = cursor.execute(f'SELECT category FROM ProductAPP_katalogmodel WHERE katalog=?',
                                     (call.data,)).fetchall()
        a = []
        if categorylar == a:
            await call.answer('Boshqa menyu mavjud emas')
        else:
            kiyimlar = InlineKeyboardMarkup()
            for i in categorylar:
                kiyimlar.add(InlineKeyboardButton(
                    text="🛍" + i[0], callback_data=i[0]))
            kiyimlar.add(InlineKeyboardButton(
                text='<<', callback_data="orqaga"))
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                                reply_markup=kiyimlar)
            await CallbackStates.katalog.set()
    except:
        await call.answer('Boshqa menyu mavjud emas')


@dp.callback_query_handler(text='orqaga_katalog')
async def orqaga_kala(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('KATALOG', reply_markup=Katalog1)


@dp.callback_query_handler(text='orqaga', state=CallbackStates.katalog)
async def mainer(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('KATALOG', reply_markup=Katalog1)
    await CallbackStates.chala.set()


@dp.callback_query_handler(state=CallbackStates.katalog)
async def catalog_oladi(call: types.CallbackQuery):
    print('Katalog ishladi')
    filters = cursor.execute(
        "SELECT id FROM ProductAPP_katalogmodel WHERE category = ?", (call.data,)).fetchall()
    category_id = filters[0][0]
    filter_sub_category = cursor.execute('SELECT sub_category FROM ProductAPP_categorymodel WHERE category_id = ?',
                                         (category_id,)).fetchall()
    buttons_list = []
    a = []
    print(filters)
    if filter_sub_category == a:
        print('Ishladi')
        await call.answer('Mahsulot Topilmadi')
    else:
        print('Else')
        button = InlineKeyboardMarkup()
        for i in filter_sub_category:
            buttons_list.append(i[0])
        for d in buttons_list:
            button.add(InlineKeyboardButton(text=d + "🛍", callback_data=d))
        button.add(InlineKeyboardButton(
            text='<<', callback_data="orqaga_katalog"))
        # await call.message.answer(f'{call.data}', reply_markup=button)
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=button)
        print(True)
        await CallbackStates.sub_catagory_state.set()


@dp.callback_query_handler(text='orqaga_katalog', state=CallbackStates.sub_catagory_state)
async def orqaga_katalog(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('KATALOG', reply_markup=Katalog1)
    await CallbackStates.chala.set()


@dp.callback_query_handler(state=CallbackStates.sub_catagory_state)
async def sub_category(call: types.CallbackQuery, state: FSMContext):
    id_subcategory = cursor.execute(f'SELECT id FROM ProductAPP_categorymodel WHERE sub_category = ?',
                                    (call.data,)).fetchone()
    print(id_subcategory)

    mahsulotlar = cursor.execute('SELECT name FROM ProductAPP_productmodel WHERE sub_category_id = ?',
                                 (id_subcategory[0],)).fetchall()
    print(mahsulotlar)
    a = []
    if id_subcategory == a:
        await call.answer('Bu Bo`limda Mahsulotlarimiz Mavjud emas')
    else:
        inline_keyboard_mahsulotlar = InlineKeyboardMarkup()
        for i in mahsulotlar:
            inline_keyboard_mahsulotlar.add(
                InlineKeyboardButton(text="🛍" + i[0], callback_data=i[0]))
        inline_keyboard_mahsulotlar.add(InlineKeyboardButton(
            text='<<', callback_data="orqaga_sub"))
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.data)
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                            reply_markup=inline_keyboard_mahsulotlar)
        await state.finish()
        await CallbackStates.product_state.set()


@dp.callback_query_handler(state=CallbackStates.product_state, text="orqaga_sub")
async def sub_orqaga(call: types.CallbackQuery):
    await call.message.delete()
    await call.message.answer('KATALOG', reply_markup=Katalog1)
    await CallbackStates.chala.set()


@dp.callback_query_handler(state=CallbackStates.product_state)
async def product_aywdfiawd(call: types.CallbackQuery, state: FSMContext):
    if call.data != 'ha':
        mahsulot_nomi = call.data
        global a
        a = cursor.execute(
            f"SELECT * FROM ProductAPP_productmodel WHERE name=?", (mahsulot_nomi,)).fetchall()
        saler_name = cursor.execute(
            f"SELECT name FROM SalerApp_salerregister WHERE id = {a[0][-2]}").fetchone()
        sub_category = cursor.execute(
            f"SELECT sub_category FROM ProductAPP_categorymodel WHERE category_id = {a[0][-1]}").fetchone()
        print(sub_category)
        description = f'''
🆔Mahsulot id: {a[0][0]}
✒️Mahsulot nomi: {a[0][1]}
💸Mahsulot narxi: {a[0][5]}
🔮Mahsulot rangi: {a[0][6]}
📄Mahsulot haqida : {a[0][7]}
📌Mahsulot o`lchami : {a[0][8]}
🛒Mahsulot qoldiqi : {a[0][9]}
👱‍♂️Sotuvchi : {saler_name[0]}    

    '''
        media_group = [
            InputMediaPhoto(media=open(
                f'../{a[0][2]}', 'rb')),
            InputMediaPhoto(media=open(
                f'../{a[0][3]}', 'rb')),
            InputMediaPhoto(media=open(
                f'../{a[0][4]}', 'rb'), caption=description)
        ]

        mahsulot_n = a[0][1]
        await call.message.answer_media_group(media=media_group)
        button = InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(text='Ha', callback_data='ha'),
                InlineKeyboardButton(text='Yoq', callback_data='yoq'),
            ]
            ]
        )
        await call.message.answer("Sotib Olmoqchimisiz", reply_markup=button)

    elif call.data == 'ha':
        await call.message.delete()
        cursor.execute(
            'INSERT INTO ProductAPP_korzinkamodel(id_mahsulot,user_id_telegram,count,status) VALUES(?,?,?,?)',
            (a[0][0], call.message.chat.id, 1, 0))
        connect.commit()

        await call.message.answer(f'Korzinkaga {a[0][1]} qo`shildi!', reply_markup=keyboard)
        await state.finish()


#
@dp.message_handler(text='Karzinka')
async def kozrinla_logic(message: types.Message):
    await message.answer("Sizning Korzinkangiz buyumlari !")
    cursor.execute("SELECT id_mahsulot FROM ProductAPP_korzinkamodel WHERE user_id_telegram=? AND status=?",
                   (message.from_user.id, 0))
    koriznkacha = cursor.fetchall()
    txt = ""
    count = 0
    umumiy_narx = 0
    for i in koriznkacha:
        count += 1
        name = cursor.execute('SELECT name FROM ProductAPP_productmodel WHERE id=?', (int(i[0]),)).fetchone()
        price = cursor.execute('SELECT price FROM ProductAPP_productmodel WHERE id=?', (int(i[0]),)).fetchone()
        umumiy_narx += price[0]
        txt += f"{count}) 📦<b>{name[0]}</b> {price[0]} So`m\n"
    txt += f"\n🤑Jami: {umumiy_narx} So`m"
    buyurmani_tasdiqlash = InlineKeyboardMarkup(row_width=1)
    buyurmani_tasdiqlash.add(InlineKeyboardButton(text="✅", callback_data="tasdiqlash"))
    buyurmani_tasdiqlash.add(InlineKeyboardButton(text="❌", callback_data="rad_qilish"))

    await message.answer(txt, parse_mode='HTML', reply_markup=buyurmani_tasdiqlash)


@dp.callback_query_handler(text="tasdiqlash")
async def tasdiqlash(call: types.CallbackQuery):
    koriznkacha = cursor.execute(
        "SELECT id_mahsulot FROM ProductAPP_korzinkamodel WHERE user_id_telegram=? AND status=?",
        (call.message.chat.id, 0))
    koriznkacha = cursor.fetchall()

    for i in koriznkacha:
        cursor.execute("INSERT INTO ProductAPP_producthistorymodel(product_id,user_id_telegram) VALUES(?,?)",
                       (i[0], call.message.chat.id))
        connect.commit()
    cursor.execute("DELETE FROM ProductAPP_korzinkamodel WHERE user_id_telegram=? AND status=?",
                   (call.message.chat.id, 0))
    connect.commit()
    await call.message.answer('Uzum punktlaridan 2 kun ichida olib keting!')


@dp.message_handler(text='Buyurtmalar tarixi!')
async def history(message: types.Message):
    history = cursor.execute(
        "SELECT product_id FROM ProductAPP_producthistorymodel WHERE user_id_telegram=?",
        (message.from_user.id,)).fetchall()
    txt = ""
    cout = 0
    for i in history:
        cout += 1
        name = cursor.execute('SELECT * FROM ProductAPP_productmodel WHERE id=?', (int(i[0]),)).fetchone()
        print(name)
        txt += f"{cout}) 📦<b>{name[1]}</b>   💵<code>{name[5]}</code>\n"
    if txt is "":
        await message.answer('Sizdahechqanday tarix mavjud emas')
    else:
        await message.answer(txt, parse_mode='HTML')


@dp.message_handler(text='Bot Haqida!', state='*')
async def bot_haqida(message: types.Message):
    await message.answer(f"""<b>It's UZUM MARKET FAKE bot !!! </b>""", parse_mode='HTML')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
