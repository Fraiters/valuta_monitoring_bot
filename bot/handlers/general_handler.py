from aiogram import Bot, Dispatcher
from aiogram.types import Message
from bot.settings import GENERAL_BUTTONS
from bot.utils.kb import Kb


class GeneralHandler:
    """Класс главных хендлеров"""

    def __init__(self, bot: Bot, ):  # db: Db):
        self.bot = bot
        self.general_kb = Kb()

    async def commands_start(self, message: Message):
        """Хендлер для команд 'start', 'help' """
        try:
            kb = self.general_kb.add(GENERAL_BUTTONS)
            await self.bot.send_message(message.from_user.id, 'С вами бот для мониторинга криптовалюты \n'
                                                              'Бот отслеживает курс криптовалюты в USD и отображает '
                                                              'его, когда он достигает минимального или максимального '
                                                              'порога.',
                                        reply_markup=kb)
        except:
            await message.reply('Общение с ботом через лс, пожалуйста напишите ему: \n @work_control_accounting_bot')

    def registration(self, dp: Dispatcher):
        """Регистрация главных хендлеров"""
        dp.register_message_handler(callback=self.commands_start, commands=['start', 'help'])
