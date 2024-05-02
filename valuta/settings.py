
# базовая ссылка на сайт
BASE_URL = "https://coinmarketcap.com/"

# ссылка на страницу с валютой
PAGE_URL = "https://coinmarketcap.com/currencies/{valuta}/"

# xpath до значения валюты
XPATH_VALUE_VALUTA = "/html/body" \
             "/div[contains(@id, '__next')]" \
             "/div[2]" \
             "/div" \
             "/div[contains(@class, 'cmc-body-wrapper')]" \
             "/div" \
             "/div" \
             "/div[contains(@data-module-name, 'Coin-stats')]" \
             "/section" \
             "/div[contains(@id, 'section-coin-overview')]" \
             "/div[contains(@data-role, 'el')]" \
             "/span/text()"
