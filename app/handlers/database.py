import sqlite3
import datetime
import os

from aiogram import Dispatcher, types


# Change this path to the path to your database
db_path = os.path.abspath(
    r"C:\Users\DosArdillas\Documents\Coding\TB\database.db")


def db_table_val(user_id: int, user_name: str, user_surname: str, username: str, date_joined):
    con = sqlite3.connect(db_path, check_same_thread=False,
                          detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    cur = con.cursor()
    cur.execute('INSERT INTO users (user_id, user_name, user_surname, username, date_joined) VALUES (?, ?, ?, ?, ?)',
                (user_id, user_name, user_surname, username, date_joined))
    con.commit()
    con.close()


async def add_to_db(message: types.Message):
    await message.answer(f'Спасибо, {message.from_user.first_name}. Ваше имя добавлено в базу данных!')

    us_id = message.from_user.id
    us_name = message.from_user.first_name
    us_sname = message.from_user.last_name
    username = message.from_user.username
    today = datetime.date.today()

    db_table_val(user_id=us_id, user_name=us_name,
                 user_surname=us_sname, username=username, date_joined=today)


def register_handlers_db(dp: Dispatcher):
    dp.register_message_handler(add_to_db, commands="database")
