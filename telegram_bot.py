import os
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot.handlers.general_handler import GeneralHandler
from bot.handlers.unknown_handler import UnknownHandler
from bot.handlers.valuta_monitoring_handler import ValutaMonitoringHandler
from bot.settings import TOKEN


class TelegramBot:
    """Класс для запуска телеграм бота"""
    # bot = Bot(token=os.getenv('TOKEN'))
    bot = Bot(token=TOKEN)

    storage = MemoryStorage()
    dp = Dispatcher(bot=bot, storage=storage)

    def run(self):
        general_handler = GeneralHandler(bot=self.bot)
        valuta_monitoring_handler = ValutaMonitoringHandler(bot=self.bot)
        unknown_handler = UnknownHandler(bot=self.bot)

        general_handler.registration(dp=self.dp)
        valuta_monitoring_handler.registration(dp=self.dp)
        unknown_handler.registration(dp=self.dp)

        executor.start_polling(dispatcher=self.dp, skip_updates=True)


if __name__ == '__main__':

    telegram_bot = TelegramBot()
    telegram_bot.run()
