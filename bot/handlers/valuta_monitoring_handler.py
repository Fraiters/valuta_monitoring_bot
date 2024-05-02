from aiogram import Bot, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import Message
from aiogram.types import ReplyKeyboardRemove

from bot.settings import GENERAL_BUTTONS
from bot.utils.kb import Kb
from valuta.valuta_monitoring import ValutaMonitoring


class FsmValutaMonitoring(StatesGroup):
    """ Класс машины состояний для мониторинга валюты """
    name_valuta = State()
    min_limit_value = State()
    max_limit_value = State()


class ValutaMonitoringHandler:
    """ Класс хендлеров для мониторинга валюты """

    def __init__(self, bot: Bot):
        self.bot = bot
        self.kb = Kb()
        self.fsm = FsmValutaMonitoring()
        self.name_valuta = ...  # type: str
        self.min_limit_value = ...  # type: int
        self.max_limit_value = ...  # type: int

    async def choose_valuta(self, message: Message):
        await self.fsm.name_valuta.set()
        await message.reply("Введите название валюты на английском", reply_markup=ReplyKeyboardRemove())

    async def load_name_valuta(self, message: Message):
        """ Загрузка названия валюты """
        self.name_valuta = message.text
        await self.fsm.min_limit_value.set()
        await self.bot.send_message(message.from_user.id, "Введите минимальный порог значения валюты",
                                    reply_markup=ReplyKeyboardRemove())

    async def load_min_lim_value(self, message: Message):
        """ Загрузка минимального порога значения валюты """
        try:
            self.min_limit_value = int(message.text)
            await self.fsm.max_limit_value.set()
            await self.bot.send_message(message.from_user.id, "Введите максимальный порог значения валюты",
                                        reply_markup=ReplyKeyboardRemove())
        except ValueError:
            await message.reply('Неверный формат записи\n'
                                'Повторите попытку')

    async def load_max_lim_value(self, message: Message, state: FSMContext):
        """ Загрузка максимального порога значения валюты"""
        try:
            self.max_limit_value = int(message.text)

            valuta_monitoring = ValutaMonitoring(name_valuta=self.name_valuta,
                                                 min_limit_value=self.min_limit_value,
                                                 max_limit_value=self.max_limit_value)

            valuta_monitoring.run()
            # (Работает только для одной валюты)

            if valuta_monitoring.status_code is False:
                await self.bot.send_message(message.from_user.id, 'Такой валюты нет\n'
                                                                  'Повторите попытку',
                                            reply_markup=ReplyKeyboardRemove())
                await self.fsm.name_valuta.set()
            else:
                kb = self.kb.add(GENERAL_BUTTONS)
                await self.bot.send_message(message.from_user.id, f"Курс {valuta_monitoring.name_valuta} достиг "
                                                                  f"{valuta_monitoring.value_valuta}", reply_markup=kb)

            await state.finish()
            kb = self.kb.add(GENERAL_BUTTONS)
            await self.bot.send_message(message.from_user.id, 'Главное меню', reply_markup=kb)

        except ValueError:
            await message.reply('Неверный формат записи\n'
                                'Повторите попытку')

    async def cancel(self, message: Message, state: FSMContext):
        """ Выход из машины состояний """
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        kb = self.kb.add(GENERAL_BUTTONS)
        await self.bot.send_message(message.from_user.id, 'Главное меню', reply_markup=kb)

    def registration(self, dp: Dispatcher):
        """ Регистрация хендлеров """
        dp.register_message_handler(callback=self.choose_valuta, commands=['Выбрать_валюту'], state=None)

        dp.register_message_handler(callback=self.cancel, commands=['Отмена'],
                                    state='*')
        dp.register_message_handler(self.cancel, Text(equals='Отмена', ignore_case=True),
                                    state='*')
        # Мониторинг валюты
        dp.register_message_handler(callback=self.load_name_valuta,
                                    state=self.fsm.name_valuta)
        dp.register_message_handler(callback=self.load_min_lim_value,
                                    state=self.fsm.min_limit_value)
        dp.register_message_handler(callback=self.load_max_lim_value,
                                    state=self.fsm.max_limit_value)
