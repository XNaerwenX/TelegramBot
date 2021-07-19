import asyncio
import sqlite3
import logging
import os
import aioschedule as schedule


logging.basicConfig(level=logging.INFO)
log = logging.getLogger('__name__')

db_path = os.path.abspath(
    r"C:\Users\DosArdillas\Documents\Coding\TB\database.db")


# Getting a list of user IDs (that have certain mail_flags set to False) from the database to mail our info
def get_mailing_list(mail_flag1, mail_flag2, mail_flag3):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("SELECT user_id FROM users WHERE mail1=? AND mail2=? AND mail3=?",
                (mail_flag1, mail_flag2, mail_flag3))
    temp = cur.fetchall()
    users_to_mail = [user[0] for user in temp]
    con.close()
    return users_to_mail


# A function to update the relevant flags from False to True so that users don't get mailed the same info more than once
def update_db(new_m_flag1, new_m_flag2, new_m_flag3, m_flag1, m_flag2, m_flag3):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("UPDATE users SET mail1=? WHERE mail1=?",
                (new_m_flag1, m_flag1))
    cur.execute("UPDATE users SET mail2=? WHERE mail2=?",
                (new_m_flag2, m_flag2))
    cur.execute("UPDATE users SET mail3=? WHERE mail3=?",
                (new_m_flag3, m_flag3))
    con.commit()
    con.close()


async def mail_one(bot):
    for user_id in get_mailing_list(False, False, False):
        try:
            await bot.send_message(chat_id=user_id, text="Good morning! Here's part one of our mailing list.")
            await bot.send_message(chat_id=user_id, text="Some info here.")
            await bot.send_message(chat_id=user_id, text="Have a nice day.")
        except Exception as e:
            print(f"{e}")
            log.exception(f"Target [ID:{user_id}]: failed")
        else:
            log.info(f"M1.Target [ID:{user_id}]: success")
            update_db(True, False, False, False, False, False)
    return schedule.CancelJob


async def mail_two(bot):
    for user_id in get_mailing_list(True, False, False):
        try:
            await bot.send_message(chat_id=user_id, text="Good morning! Here's part two of our mailing list.")
            await bot.send_message(chat_id=user_id, text="Some more info here.")
            await bot.send_message(chat_id=user_id, text="Have a nice day.")
        except Exception as e:
            print(f"{e}")
            log.exception(f"Target [ID:{user_id}]: failed")
        else:
            log.info(f"M2.Target [ID:{user_id}]: success")
            update_db(True, True, False, True, False, False)
    return schedule.CancelJob


async def mail_three(bot):
    for user_id in get_mailing_list(True, True, False):
        try:
            await bot.send_message(chat_id=user_id, text="Good morning! Here's part three of our mailing list.")
            await bot.send_message(chat_id=user_id, text="Even MORE info here.")
            await bot.send_message(chat_id=user_id, text="Have a nice day.")
        except Exception as e:
            print(f"{e}")
            log.exception(f"Target [ID:{user_id}]: failed")
        else:
            log.info(f"M3.Target [ID:{user_id}]: success")
            update_db(True, True, True, True, True, False)
    return schedule.CancelJob
