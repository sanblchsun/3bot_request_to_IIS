from random import randint
from config import BOT_TOKEN
import logging
from keyboards.default.menu import button_generator_kod_access

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor


class Form(StatesGroup):
    state0 = State()
    state1 = State()
    state2 = State()
    state3 = State()
    state4 = State()
    state5 = State()
    state6 = State()
    state7 = State()


logging.basicConfig(level=logging.INFO)


bot = Bot(token=BOT_TOKEN, validate_token=True, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

dict_chat = {}


async def generator_kod_access(current_chat_id):
    i = 0
    while True:
        id_access = randint(100, 999)
        if dict_chat[id_access] is None:
            dict_chat[id_access] = current_chat_id
            return id_access
        if (i += 1) > 2000:
            await message.answer('Непредвиденная ошибка, \
                свяжитесь с разработчиком, код ошибки "while infinity"')


@dp.message_handler(state='*', commands=['start'])
async def bot_start(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
    state = dp.current_state(user=message.from_user.id)
    await Form.state0.set()
    await message.answer(f"Привет, {message.from_user.full_name}! \n \
         что бы создать приватный чат, \n нажмите на ссылку /chat",
                         reply_markup=types.ReplyKeyboardRemove())
    current_state = await state.get_state()
    logging.info(f'start, current_state: {current_state} !!!!!!!')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    logging.info(f'Заявка отменена и обнулены все данные для чата \
                 message.chat.id: {message.chat.id}')
    await state.finish()
    await message.reply('Вы отменили заявку, \
        что бы отправить новую заявку, \n нажмите на ссылку /start',
                        reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(state=Form.state0, commands=['chat'])
async def def_start(message: types.Message, state: FSMContext):
    markup = await button_generator_kod_access()
    await message.answer('Нажмите кнопку ниже и создайте код доступа',
                         reply_markup=markup)
    await Form.state1.set()
    logging.info(
        f'state=0, message.chat.id: {message.chat.id}, \
        message.message_id: {message.message_id}')


@dp.message_handler(state=Form.state1)
async def action_stat1(message: types.Message, state: FSMContext):
    if message.text == 'создать код чата 🆔':
        id_access = await generator_kod_access(message.chat.id)
        await message.answer(f'Сообщите собеседнику код: {id_access}',
                             reply_markup=types.ReplyKeyboardRemove())
        logging.info(
            f'state=1, message.chat.id: {message.chat.id}, \
        message.message_id: {message.message_id}')
    else:
        return


@dp.message_handler(state='*', content_types=types.ContentTypes.ANY)
async def action_state_all(message: types.Message, state: FSMContext):
    logging.info(
        f'state = {current_state}, message.chat.id: {message.chat.id}, \
        message.message_id: {message.message_id}')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
