import sqlite3
import os

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup


class Feedback(StatesGroup):
    waiting_for_feedback = State()


db_path = os.path.abspath(
    r"C:\Users\DosArdillas\Documents\Coding\TB\database.db")


def db_table_val(user_id: int, feedback: str):
    con = sqlite3.connect(db_path, check_same_thread=False,
                          detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()

    cur.execute('INSERT INTO feedback (user_id, feedback) VALUES (?, ?)',
                (user_id, feedback))
    con.commit()
    con.close()


async def start_feedback(message: types.Message):
    await message.answer("Добро пожаловать в секцию обратной связи! Напишите свой отзыв:")
    await Feedback.waiting_for_feedback.set()


async def send_feedback(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text.lower())

    us_id = message.from_user.id
    fb = message.text

    db_table_val(user_id=us_id, feedback=fb)

    await message.answer(f"Спасибо за отзыв!")
    await state.finish()


def register_handlers_feedback(dp: Dispatcher):
    dp.register_message_handler(
        start_feedback, commands="feedback", state="*")
    dp.register_message_handler(
        send_feedback, state=Feedback.waiting_for_feedback)
