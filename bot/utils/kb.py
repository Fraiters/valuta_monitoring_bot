from aiogram.types import ReplyKeyboardMarkup
from typing import List
from bot.utils.button import Button


class Kb:
    """Класс для управления клавиатурой """
    kb = ...  # type: ReplyKeyboardMarkup

    def __init__(self):
        self.button = Button()

    def add(self, names_buttons: List[str]):
        """Добавление кнопок

        :param names_buttons: список добавляемых кнопок
        :return: объект клавиатуры
        """
        self.button.add(names=names_buttons)
        self.kb = self.button.kb
        return self.kb
