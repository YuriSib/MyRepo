import json
import requests
from config import keys

class APIException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise APIException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_tiсker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}.')

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}.')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_tiсker}&tsyms={base_ticker}')
        r = requests.get(f'WkgnuuRlz1M2noA46hAQ7a6BtfvAFXAtRX4XRpJa WkgnuuRlz1M2noA46hAQ7a6BtfvAFXAtRX4XRpJa')
        total_base = json.loads(r.content)[keys[base]]

        return total_base
