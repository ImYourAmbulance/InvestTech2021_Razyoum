import logging
import os
from sys import exit
from aiogram.types import *
from get_data import unique_names, total_profit, price
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

TOKEN = '2110630973:AAHkLE2j1jOOgTrajs0QJTPzd03mXuB62Dk'
if not TOKEN:
    exit('Error: no token provided')

WEBHOOK_HOST = 'https://obli-bot.herokuapp.com'
WEBHOOK_PATH = f'/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
HOST = '0.0.0.0'
PORT = int(os.environ.get('PORT', 5001))
# data = ['Sberbank', 'Delimobil', 'Rosneft', 'Phaizer', 'ObligaciiRF', 'RZD', 'GOSDOLG USA', 'MorgensternCoin', 'MoyaSamoochenka', 'WayrmaRossii']

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` command
    """
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('📁 Список облигаций')
    keyboard.add('💼 Собрать портфель')
    await message.answer("Привет, меня зовут Бонд, Джеймс Бонд.\n"
                         "Я помогу вам с облигациями.\n", reply_markup=keyboard)


@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    '''
    This handler will be called when user sends `/help` command
    :param message:
    :return:
    '''
    await message.answer("Help here!")


@dp.message_handler(lambda message: message.text == '💼 Собрать портфель')
async def pack_bag(message: types.Message):
    await message.answer('Собираем портфель....')


@dp.message_handler(lambda message: message.text == '📁 Список облигаций')
async def show_bonds(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = []
    for bond in range(0, len(unique_names)):
        buttons.append(InlineKeyboardButton(f'{unique_names[bond]}', callback_data=f'{unique_names[bond]}'))
    keyboard.add(*buttons)
    keyboard.add(InlineKeyboardButton(f'←', callback_data=f'<<'), InlineKeyboardButton('1 / 1', callback_data='page_number'), InlineKeyboardButton(f'→', callback_data=f'>>'))
    await message.answer('Выберите облигацию, которую хотите посмотреть:', reply_markup=keyboard)


@dp.callback_query_handler(text='<<')
async def func5(call: types.CallbackQuery):
    await call.answer()


@dp.callback_query_handler(text='>>')
async def func6(call: types.CallbackQuery):
    await call.answer()


@dp.callback_query_handler(text='page_number')
async def func7(call: types.CallbackQuery):
    await call.answer()


@dp.callback_query_handler(text=unique_names)
async def func1(call: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton(f'Подсчитать прибыль для облигации', callback_data=f'{call.data}1'),
        types.InlineKeyboardButton(f'Узнать стоимость покупки облигации', callback_data=f'{call.data}2')
    ]
    keyboard.add(*buttons)
    await call.message.answer(f'{call.data}', reply_markup=keyboard)
    await call.answer()


@dp.callback_query_handler(text=[bond+'1' for bond in unique_names])
async def func3(call: types.CallbackQuery):
    await call.message.answer(f'Прибыль с облигации - {total_profit}')
    await call.answer()


@dp.callback_query_handler(text=[bond+'2' for bond in unique_names])
async def func4(call: types.CallbackQuery):
    await call.message.answer(f"Стоимость облигации - {price}")
    await call.answer()


@dp.message_handler()
async def nothing(message: types.Message):
    # old style:
    # await bot.send_message(message.chat.id, message.text)
    await message.answer('Я не знаю такой команды.')


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    logging.warning('Bot started....')


async def on_shutdown(dp):
    logging.warning('Bot shutting down....')
    # await bot.delete_webhook()


if __name__ == '__main__':
    # print(unique_names)
    # print(type(unique_names))
    executor.start_polling(dp, skip_updates=True)  #
    # executor.start_webhook(dispatcher=dp,
    #                      webhook_path=WEBHOOK_PATH,
     #                      on_startup=on_startup,
      #                     on_shutdown=on_shutdown,
       #                    host=HOST,
        #                   port=PORT)
