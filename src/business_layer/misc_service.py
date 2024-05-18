import requests

from src.constants.messages import OK
from src.utilities.utils import config, get_error_message


def get_token_rate(base_token_symbol: str, quote_token_symbol: str):
    try:
        if base_token_symbol not in [''] and quote_token_symbol not in ['']:
            response = requests.get(config['CryptoPaymentGateway']['BaseURL'] + 'get_currencies_rates?from_currency_symbols=' + base_token_symbol + '&to_currency_symbols='+quote_token_symbol)

            crypto_data = response.json()
            rate = crypto_data['data'][base_token_symbol][quote_token_symbol]
            print(rate)
            return {'success': True, 'message': OK, 'rate': rate}

        return {'success': False, 'message': 'Cannot fetch rate for custom token!'}
    except Exception as e:
        print(e.__str__())
        return {'success': False, 'message': get_error_message(e)}

