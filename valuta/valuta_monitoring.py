import re
import time
import requests
import lxml.html

from valuta.settings import PAGE_URL, XPATH_VALUE_VALUTA


class ValutaMonitoring:
    """ Класс мониторинга валюты """

    def __init__(self, name_valuta: str, min_limit_value: int, max_limit_value: int):

        self.name_valuta = name_valuta.lower()
        self.min_limit_value = min_limit_value
        self.max_limit_value = max_limit_value
        self.value_valuta = ...  # type: str
        self.status_code = True

    def get_value_from_html_content(self, html_content: str, xpath: str):
        """ Получение значения из html контента по xpath"""
        tree = lxml.html.document_fromstring(html_content)
        value = tree.xpath(xpath)[0]
        return value

    def set_value_valuta(self):
        """ Установка значения валюты"""

        # составление url ссылки до страницы конкретной валюты
        url = PAGE_URL.format(valuta=self.name_valuta)
        # запрос на данные одной html-страницы
        response = requests.get(url=url)

        # проверка статуса кода
        if response.status_code == 404:
            self.status_code = False
            return -1

        # заполнение html-текста страницы и перевод в формат строки
        html_content = str(response.content.decode(encoding='utf-8', errors='strict'))

        self.value_valuta = self.get_value_from_html_content(html_content=html_content,
                                                             xpath=XPATH_VALUE_VALUTA)
        # print(self.value_valuta, "Поток: ", self.name_valuta)

    def check_value_valuta_for_lim(self) -> bool:
        """ Проверка значения валюты на предел"""
        # перевод значения валюты в тип float
        value_valuta_float = float(re.sub(r'[^\d.]', '', self.value_valuta))
        if self.min_limit_value < value_valuta_float < self.max_limit_value:
            return True

    def run(self):
        self.set_value_valuta()

        if self.status_code is False:
            return -1

        while self.check_value_valuta_for_lim():
            self.set_value_valuta()
            time.sleep(1)
        # print("Конец")


if __name__ == '__main__':
    valuta_monitoring = ValutaMonitoring(name_valuta="bitcoin", min_limit_value=57600, max_limit_value=57800)

    valuta_monitoring2 = ValutaMonitoring(name_valuta="ethereum", min_limit_value=56600, max_limit_value=56800)

    from threading import Thread

    th1 = Thread(target=valuta_monitoring.run)
    th2 = Thread(target=valuta_monitoring2.run)

    thread_pool = [th1, th2]

    for thread in thread_pool:
        thread.start()
