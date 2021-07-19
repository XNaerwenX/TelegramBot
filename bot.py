import asyncio
import logging
import aioschedule as schedule

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.config_reader import load_config
from app.handlers.poll import register_handlers_poll
from app.handlers.common import register_handlers_common
from app.handlers.database import register_handlers_db
from app.handlers.feedback import register_handlers_feedback
from app.handlers.mailing import mail_one, mail_two, mail_three
from app.handlers.stickers import morning, evening

logger = logging.getLogger(__name__)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="/feedback",
                   description="Отправить нам сообщение"),
        BotCommand(command="/poll", description="Пройти опрос"),
        BotCommand(command="/database",
                   description="Подписаться на рассылку"),
        BotCommand(command="/cancel", description="Отмена")
    ]
    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")

    # Parsing the config file
    config = load_config("config/bot.ini")

    # Instantiating Bot and Dispatcher objects
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    async def scheduler():
        # This line is here temporarily for debugging/checking if it works
        schedule.every(5).seconds.do(lambda: mail_one(bot))
        schedule.every().day.at('10:00').do(lambda: mail_one(bot))
        schedule.every().day.at('21:30').do(lambda: mail_two(bot))
        schedule.every().day.at('10:00').do(lambda: mail_three(bot))
        while True:
            await schedule.run_pending()
            await asyncio.sleep(1)

    await set_commands(bot)

    # Registering handlers
    register_handlers_common(dp, config.tg_bot.admin_id)
    register_handlers_feedback(dp)
    register_handlers_db(dp)
    register_handlers_poll(dp)

    # optional: await dp.skip_updates()
    asyncio.create_task(scheduler())
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
