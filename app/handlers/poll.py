import sqlite3
import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


db_path = os.path.abspath(
    r"C:\Users\DosArdillas\Documents\Coding\TB\database.db")


def db_table_val(user_id: int, Q1: str, Q2: str):
    con = sqlite3.connect(db_path, check_same_thread=False,
                          detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute('INSERT OR REPLACE INTO poll (user_id, Q1, Q2) VALUES (?, ?, ?)',
                (user_id, Q1, Q2))
    con.commit()
    con.close()


available_answers_q1 = ["a", "b", "c"]
available_answers_q2 = ["d", "e", "f"]


class TakePoll(StatesGroup):
    waiting_for_answer_q1 = State()
    waiting_for_answer_q2 = State()


async def poll_start(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for var in available_answers_q1:
        keyboard.add(var)
    await message.answer("Вопрос №1. Выберите вариант ответа:", reply_markup=keyboard)
    await TakePoll.waiting_for_answer_q1.set()


async def question_one(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_answers_q1:
        await message.answer("Пожалуйста, выберите вариант ответа, используя клавиатуру ниже.")
        return
    await state.update_data(chosen_var=message.text.lower())

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in available_answers_q2:
        keyboard.add(item)

    await TakePoll.next()
    await message.answer("Вопрос №2. Выберите вариант ответа:", reply_markup=keyboard)


async def question_two(message: types.Message, state: FSMContext):
    if message.text.lower() not in available_answers_q2:
        await message.answer("Пожалуйста, выберите вариант ответа, используя клавиатуру ниже.")
        return
    user_data = await state.get_data()
    us_id = message.from_user.id
    Q_1 = user_data['chosen_var']
    Q_2 = message.text.lower()

    db_table_val(user_id=us_id, Q1=Q_1, Q2=Q_2)

    await message.answer(f"{user_data['chosen_var']}, {message.text.lower()}.\n"
                         f"Спасибо, что прошли наш опрос!", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


def register_handlers_poll(dp: Dispatcher):
    dp.register_message_handler(poll_start, commands="poll", state="*")
    dp.register_message_handler(
        question_one, state=TakePoll.waiting_for_answer_q1)
    dp.register_message_handler(
        question_two, state=TakePoll.waiting_for_answer_q2)
